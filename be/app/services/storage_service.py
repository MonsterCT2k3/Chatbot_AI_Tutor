import boto3
from starlette.concurrency import run_in_threadpool

from app.config import settings

_client = boto3.client(
    "s3",
    endpoint_url=settings.R2_ENDPOINT_URL,
    aws_access_key_id=settings.R2_ACCESS_KEY_ID,
    aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    region_name="auto",
)


async def upload_file(file_bytes: bytes, key: str, content_type: str | None = None) -> None:
    # boto3 is a blocking library — run it in a thread so it doesn't stall
    # the event loop (and every other concurrent request) while it uploads.
    extra_args = {"ContentType": content_type} if content_type else {}
    await run_in_threadpool(_client.put_object, Bucket=settings.R2_BUCKET_NAME, Key=key, Body=file_bytes, **extra_args)


async def download_file(key: str) -> bytes:
    response = await run_in_threadpool(_client.get_object, Bucket=settings.R2_BUCKET_NAME, Key=key)
    return await run_in_threadpool(response["Body"].read)


def get_presigned_url(key: str, expires_in: int = 3600) -> str:
    # Local signing only, no network call to R2 — safe to call directly (no threadpool needed).
    return _client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.R2_BUCKET_NAME, "Key": key},
        ExpiresIn=expires_in,
    )


async def delete_file(key: str) -> None:
    await run_in_threadpool(_client.delete_object, Bucket=settings.R2_BUCKET_NAME, Key=key)
