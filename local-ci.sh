#!/bin/bash

set -euo pipefail

export HOME=/tmp
export XDG_CACHE_HOME=/tmp/.cache
export UV_CACHE_DIR=/tmp/.uv-cache
export PYTHONDONTWRITEBYTECODE=1
export COVERAGE_FILE=reports/.coverage

echo "=== [0/5] Project installation ==="
uv sync

rm -rf reports
mkdir -p reports

echo "=== [1/5] Formatting check (Black) ==="
black --check src tests nrtests

echo "=== [2/5] Unit tests ==="
coverage run --source=src -m pytest tests -v -p no:cacheprovider \
    --html=reports/unit-tests.html --self-contained-html

echo "=== [3/5] Integration tests ==="
coverage run -a --source=src -m pytest nrtests -v -p no:cacheprovider \
    --html=reports/integration-tests.html --self-contained-html

echo "=== [4/5] Code coverage ==="
coverage report -m
coverage html -d reports/coverage


echo "=== [5/5] Security tests ==="
if ! bandit -r src -f html -o reports/security_report.html; then
    echo "Warning : Security issue(s) detected - reports/security_report.html"
    exit 1
fi

echo "=== Local CI completed successfully ==="
echo "    Unit tests      : reports/unit-tests.html"
echo "    Integration tests  : reports/integration-tests.html"
echo "    Code coverage   : reports/coverage/index.html"
echo "    Security tests    : reports/security_report.html"
