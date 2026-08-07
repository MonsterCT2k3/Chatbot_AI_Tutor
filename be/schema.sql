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

-- ivfflat index for cosine similarity search.
-- lists=100 is a reasonable default for tens of thousands of rows;
-- retune (and REINDEX) as the table grows.
create index idx_chunks_embedding on document_chunks
    using ivfflat (embedding vector_cosine_ops) with (lists = 100);

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
