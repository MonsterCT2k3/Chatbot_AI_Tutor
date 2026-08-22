"""One-off: apply a CORS policy to the R2 bucket so browsers can fetch
presigned document URLs directly (GET /documents/{id}/file returns a
presigned R2 URL that the frontend's react-pdf loads client-side).

The bucket already had a policy scoped to http://localhost:3000/GET (matches
fe/vite.config.js's dev port) -- but it was still missing what react-pdf
actually needs: the `Range` request header (byte-range fetches, so it
doesn't download the whole PDF just to render one page) and exposing
Content-Range/Accept-Ranges on the response. This adds those without
widening the origin restriction that was already deliberately there.

NOTE: the R2 API token currently in .env only has Object Read & Write scope,
not Admin Write, so PutBucketCors fails with AccessDenied -- this script
needs a token with Admin Read & Write to actually run; otherwise apply the
same policy via the Cloudflare dashboard (R2 -> bucket -> Settings -> CORS).
Update AllowedOrigins here (and on the dashboard) once there's a real
production frontend domain -- localhost:3000 alone won't cover it.

Run once per bucket: python -m scripts.setup_r2_cors
Safe to re-run -- put_bucket_cors replaces the whole policy each time.
"""

from app.services.storage_service import _client
from app.config import settings

CORS_CONFIG = {
    "CORSRules": [
        {
            "AllowedOrigins": ["http://localhost:3000"],
            "AllowedMethods": ["GET", "HEAD"],
            "AllowedHeaders": ["Range"],
            "ExposeHeaders": ["Content-Range", "Content-Length", "Accept-Ranges"],
            "MaxAgeSeconds": 3600,
        }
    ]
}

if __name__ == "__main__":
    _client.put_bucket_cors(Bucket=settings.R2_BUCKET_NAME, CORSConfiguration=CORS_CONFIG)
    result = _client.get_bucket_cors(Bucket=settings.R2_BUCKET_NAME)
    print(f"CORS applied to bucket '{settings.R2_BUCKET_NAME}':")
    print(result["CORSRules"])
