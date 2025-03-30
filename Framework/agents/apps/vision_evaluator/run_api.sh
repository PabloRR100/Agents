#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

"${SCRIPT_DIR}/.venv/bin/uvicorn" \
    main:app \
    --host 0.0.0.0 \
    --port 8000
