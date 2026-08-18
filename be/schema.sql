-- ============================================================
-- AI TUTOR — INITIAL DATABASE SCHEMA
-- Target: Supabase Postgres (pgvector enabled)
-- Auth & authorization handled in FastAPI (not Supabase Auth/RLS)
-- Design goal: minimal MVP surface, but extensible without breaking changes
-- ============================================================

-- Required extensions
create extension if not exists "uuid-ossp";
create extension if not exists vector;

-- ------------------------------------------------------------
-- 1. USERS
-- Managed entirely by FastAPI (own JWT + password hashing).
-- ------------------------------------------------------------
create table users (
    id              uuid primary key default gen_random_uuid(),
    email           text unique not null,
    hashed_password text not null,
    name            text,
    -- extensibility: free-form settings without new migrations later
    -- (e.g. { "preferred_language": "vi", "theme": "dark" })
    settings        jsonb not null default '{}',
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

-- ------------------------------------------------------------
-- 2. DOCUMENTS
-- One row per uploaded PDF/PPTX. File itself lives in R2 —
-- this table only stores the reference (object key), not the blob.
-- ------------------------------------------------------------
create table documents (
    id              uuid primary key default gen_random_uuid(),
    user_id         uuid not null references users(id) on delete cascade,

    filename        text not null,
    file_type       text not null check (file_type in ('pdf', 'pptx')),
    file_size_bytes bigint,

    -- R2 object key, e.g. "documents/{user_id}/{document_id}/original.pdf"
    storage_key     text not null,
    -- optional: object key of a lightweight preview asset if generated
    thumbnail_key   text,
    -- only set for PPTX uploads: R2 key of the PDF LibreOffice converted it to
    converted_pdf_key text,

    page_count      int,

    -- ingestion lifecycle: pending -> parsing -> embedding -> ready | failed
    status          text not null default 'pending'
                        check (status in ('pending','parsing','embedding','ready','failed')),
    error_message   text,

    -- extensibility: model/version used for embeddings, parser version, etc.
    -- avoids adding new columns every time the pipeline changes
    metadata        jsonb not null default '{}',

    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

create index idx_documents_user on documents(user_id, created_at desc);
create index idx_documents_status on documents(status);

-- ------------------------------------------------------------
-- 3. DOCUMENT PAGES
-- One row per page (PDF) or slide (PPTX). Backs the viewer +
-- gives citations something stable to point to.
-- ------------------------------------------------------------
create table document_pages (
    id              uuid primary key default gen_random_uuid(),
    document_id     uuid not null references documents(id) on delete cascade,

    page_number     int not null,
    raw_text        text,              -- full extracted text for this page/slide
    thumbnail_key   text,              -- R2 key of rendered page image

    -- extensibility: layout info, OCR confidence, detected tables/images, etc.
    metadata        jsonb not null default '{}',

    unique(document_id, page_number)
);

create index idx_pages_document on document_pages(document_id);

-- ------------------------------------------------------------
-- 4. DOCUMENT CHUNKS + EMBEDDINGS
-- The retrieval unit for RAG. Vector lives in the same row as
-- the text + page reference — keeps retrieval + citation resolution
-- to a single query instead of joining across services.
-- ------------------------------------------------------------
create table document_chunks (
    id              uuid primary key default gen_random_uuid(),
    document_id     uuid not null references documents(id) on delete cascade,
    page_id         uuid not null references document_pages(id) on delete cascade,
    page_number     int not null,       -- denormalized for fast filtering/highlighting

    chunk_index     int not null,       -- order within the page
    content         text not null,
    token_count     int,

    -- optional fine-grained highlight box: {"x":..,"y":..,"w":..,"h":..}
    bbox            jsonb,

    -- 1536 = OpenAI text-embedding-3-small / similar dim.
    -- If you switch embedding models later, add a new column
    -- (e.g. embedding_v2 vector(N)) rather than migrating this one in place.
    embedding       vector(1536),

    created_at      timestamptz not null default now()
);

create index idx_chunks_document on document_chunks(document_id);
create index idx_chunks_page on document_chunks(page_id);

-- No ivfflat/HNSW index on embedding on purpose: an ivfflat index with
-- lists=100 was tried and dropped (migration 5e27bd66a382) after it was
-- found to silently return ZERO rows for ~14% of real queries on a table
-- this small (~170 rows) -- too many lists for too little data, some
-- clusters ended up empty and the default probes=1 missed them entirely.
-- Plain sequential scan is fast AND exact (no ANN approximation) at this
-- scale. Revisit only once a document's chunk count is large enough
-- (thousands+) that an ANN index is actually justified -- see
-- explain-logic/phase-5.6-guardrails-observability/5.6.3.

-- ------------------------------------------------------------
-- 5. CHAT SESSIONS
-- Multi-session support: many chats per document, per user.
-- ------------------------------------------------------------
create table chat_sessions (
    id              uuid primary key default gen_random_uuid(),
    user_id         uuid not null references users(id) on delete cascade,
    document_id     uuid not null references documents(id) on delete cascade,

    title           text not null default 'New chat',

    -- extensibility: pinned, archived, model used, temperature, etc.
    metadata        jsonb not null default '{}',

    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

create index idx_sessions_user on chat_sessions(user_id, updated_at desc);
create index idx_sessions_document on chat_sessions(document_id);

-- ------------------------------------------------------------
-- 6. CHAT MESSAGES
-- ------------------------------------------------------------
create table chat_messages (
    id              uuid primary key default gen_random_uuid(),
    session_id      uuid not null references chat_sessions(id) on delete cascade,

    role            text not null check (role in ('user','assistant')),
    content         text not null,

    -- extensibility: token usage, model name, latency_ms, retrieval params —
    -- useful later for cost tracking/debugging without new columns
    metadata        jsonb not null default '{}',

    created_at      timestamptz not null default now()
);

create index idx_messages_session on chat_messages(session_id, created_at);

-- ------------------------------------------------------------
-- 7. MESSAGE CITATIONS
-- Links an assistant message back to the exact chunk/page it used.
-- This is what drives "highlight the referenced page/slide" in the UI.
-- ------------------------------------------------------------
create table message_citations (
    id              uuid primary key default gen_random_uuid(),
    message_id      uuid not null references chat_messages(id) on delete cascade,
    document_id     uuid not null references documents(id) on delete cascade,
    chunk_id        uuid references document_chunks(id) on delete set null,

    page_number     int not null,
    snippet         text,               -- short excerpt shown in the citation card

    created_at      timestamptz not null default now()
);

create index idx_citations_message on message_citations(message_id);
create index idx_citations_document on message_citations(document_id);

-- ------------------------------------------------------------
-- 8. REFRESH TOKENS
-- Backs real session revocation (logout, "log out this session") —
-- access tokens are short-lived and stateless, refresh tokens are the
-- only thing that can actually be killed server-side before it expires.
-- ------------------------------------------------------------
create table refresh_tokens (
    id              uuid primary key default gen_random_uuid(),
    user_id         uuid not null references users(id) on delete cascade,

    -- SHA-256 of the raw token — random high-entropy string, so a fast
    -- hash is enough (unlike passwords, which need slow hashing like bcrypt).
    token_hash      text not null,
    expires_at      timestamptz not null,
    revoked         boolean not null default false,

    created_at      timestamptz not null default now()
);

create index idx_refresh_tokens_user on refresh_tokens(user_id);
create index idx_refresh_tokens_hash on refresh_tokens(token_hash);

-- ------------------------------------------------------------
-- 9. AI USAGE LOG
-- One row per ask() call, including calls a guardrail blocked. Backs the
-- per-user daily quota (5.6.6), token/cost tracking (5.6.7), and, later, the
-- abuse circuit breaker (5.6.8).
--
-- Deliberately NOT derived from chat_messages: that table is tied to
-- chat_sessions (Phase 6) and only records successful turns, whereas quota
-- must also count blocked calls -- otherwise spamming harmful input would
-- cost the attacker no quota at all while still costing real money on
-- moderation/embedding.
-- ------------------------------------------------------------
create table ai_usage_log (
    id                  uuid primary key default gen_random_uuid(),
    user_id             uuid not null references users(id) on delete cascade,
    -- SET NULL, not CASCADE: deleting a document must not erase usage history
    -- (quota already spent cannot be refunded).
    document_id         uuid references documents(id) on delete set null,

    -- Outcome of the call. Enough to answer "which guardrail blocks most" and
    -- "how often do we retry" without storing the question/answer text itself
    -- (avoid holding user content until there is a real need for it).
    blocked_reason      text,       -- 'input_moderation' | 'output_moderation' | null
    grounded            boolean,
    faithfulness_score  double precision,
    retried             boolean,

    -- 5.6.7: real token usage + estimated USD cost for this one call
    -- (generation + judge, doubled if retried). Estimated from a published
    -- price table at code time, not an actual invoice line.
    total_tokens        integer not null default 0,
    estimated_cost_usd  double precision not null default 0,

    created_at          timestamptz not null default now()
);

-- Serves both 5.6.6 ("how many calls since midnight") and 5.6.8 ("... in the
-- last 5 minutes") -- same shape, only the time bound differs.
create index idx_ai_usage_user_time on ai_usage_log(user_id, created_at);

-- ------------------------------------------------------------
-- 10. AI CALL LOG (5.6.9)
-- One row per REAL LLM/moderation API call (not per ask() call like
-- ai_usage_log above) -- a single question with a retry produces 4 rows here
-- (generation, judge, generation again, judge again) but only 1 row in
-- ai_usage_log. This is the data debugging answer QUALITY needs: the actual
-- prompt/response text and latency, which ai_usage_log deliberately omits.
--
-- No hard FK to ai_usage_log: rows here are written the moment each API call
-- happens, DURING ask() -- before ask_for_user() creates the corresponding
-- ai_usage_log row afterwards. A real FK would fail (parent doesn't exist
-- yet at insert time). call_group_id (generated once per ask() call, and
-- reused by ask_for_user as the ai_usage_log row's own id) is a soft link
-- instead -- joinable in application code, not enforced at the DB level.
-- ------------------------------------------------------------
create table ai_call_log (
    id                  uuid primary key default gen_random_uuid(),
    call_group_id       uuid not null,

    call_type           text not null,  -- 'generation' | 'judge' | 'input_moderation' | 'output_moderation'
    model               text,
    prompt_version      text,

    -- Real content, truncated (see MAX_LOGGED_TEXT_LENGTH in usage_service.py)
    -- so one long RAG context doesn't get duplicated into every log row.
    prompt              text,
    response            text,

    latency_ms          double precision not null,
    prompt_tokens       integer not null default 0,
    completion_tokens   integer not null default 0,
    estimated_cost_usd  double precision not null default 0,

    created_at          timestamptz not null default now()
);

create index idx_ai_call_group on ai_call_log(call_group_id);
create index idx_ai_call_created on ai_call_log(created_at);

-- ------------------------------------------------------------
-- 11. ANSWER FEEDBACK (5.6.12)
-- 👍/👎 + optional reason, attached to exactly one answer via ai_usage_log_id.
-- Unlike ai_call_log, this IS a real hard FK: feedback can only be submitted
-- AFTER the user has already received the answer, so the parent ai_usage_log
-- row is guaranteed to exist by the time this row is inserted -- no "child
-- written before parent" ordering problem here.
-- ------------------------------------------------------------
create table answer_feedback (
    id                  uuid primary key default gen_random_uuid(),
    ai_usage_log_id     uuid not null references ai_usage_log(id) on delete cascade,
    user_id             uuid not null references users(id) on delete cascade,

    is_positive         boolean not null,
    reason              text,

    created_at          timestamptz not null default now(),

    -- One user has exactly one CURRENT opinion per answer -- resubmitting
    -- updates in place rather than piling up history rows (see
    -- usage_service.submit_feedback), so aggregates never double-count.
    unique (ai_usage_log_id, user_id)
);

create index idx_answer_feedback_log on answer_feedback(ai_usage_log_id);

-- ------------------------------------------------------------
-- updated_at auto-touch trigger (reused across tables)
-- ------------------------------------------------------------
create or replace function set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

create trigger trg_users_updated_at
    before update on users
    for each row execute function set_updated_at();

create trigger trg_documents_updated_at
    before update on documents
    for each row execute function set_updated_at();

create trigger trg_sessions_updated_at
    before update on chat_sessions
    for each row execute function set_updated_at();
