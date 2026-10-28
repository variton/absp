#!/bin/bash

set -euo pipefail

cd /absp

export HOME=/tmp
export XDG_CACHE_HOME=/tmp/.cache
export UV_CACHE_DIR=/tmp/.uv-cache
export PYTHONDONTWRITEBYTECODE=1
export COVERAGE_FILE=/absp/reports/.coverage


echo
echo "=== [0/4] Project installation ==="
uv sync

rm -rf reports
mkdir -p reports

echo "=== [1/4] Formatting check (Black) ==="
black --check src tests nrtests

echo "=== [2/4] Unit tests ==="
coverage run --source=src -m pytest tests -v -p no:cacheprovider \
    --html=reports/unit-tests.html --self-contained-html

echo "=== [3/4] Integration tests ==="
coverage run -a --source=src -m pytest nrtests -v -p no:cacheprovider \
    --html=reports/integration-tests.html --self-contained-html

echo "=== [4/4] Code coverage ==="
coverage report -m
coverage html -d reports/coverage

echo "=== Local CI completed successfully ==="
echo "    Unit tests      : reports/unit-tests.html"
echo "    Integration tests  : reports/integration-tests.html"
echo "    Code coverage   : reports/coverage/index.html"
