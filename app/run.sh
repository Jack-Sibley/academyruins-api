#!/usr/bin/env bash
set -eo pipefail

# ensure app\resources\generated and app\static\raw_docs\ are present
mkdir -p resources/generated
mkdir -p static/raw_docs/

# mount GCS buckets
gcsfuse --debug_gcs --debug_fuse --only-dir generated/ ancestral-vision-storage resources/generated/
gcsfuse --debug_gcs --debug_fuse --only-dir raw_docs/ ancestral-vision-storage static/raw_docs/

# run the app
poetry run uvicorn main:app --proxy-headers --host 0.0.0.0 --port 80

wait -n