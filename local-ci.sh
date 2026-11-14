#!/bin/bash

set -euo pipefail

export HOME=/tmp
export XDG_CACHE_HOME=/tmp/.cache
export UV_CACHE_DIR=/tmp/.uv-cache
export PYTHONDONTWRITEBYTECODE=1
export COVERAGE_FILE=reports/.coverage

echo "=== [0/6] Project installation ==="
uv sync

rm -rf reports
mkdir -p reports

echo "=== [1/6] Formatting check (Black) ==="
black --check src tests nrtests

echo "=== [2/6] Unit tests ==="
coverage run --source=src -m pytest tests -v -p no:cacheprovider \
    --html=reports/unit-tests.html --self-contained-html

echo "=== [3/6] Integration tests ==="
coverage run -a --source=src -m pytest nrtests -v -p no:cacheprovider \
    --html=reports/integration-tests.html --self-contained-html

echo "=== [4/6] Code coverage ==="
coverage report -m
coverage html -d reports/coverage


echo "=== [5/6] Security tests ==="
if ! bandit -r src -f html -o reports/security_report.html; then
    echo "Warning : Security issue(s) detected - reports/security_report.html"
    exit 1
fi

echo "=== [6/6] Documentation (Sphinx) ==="
rm -rf sphinx/modules
rm -rf docs/documentation
sphinx-apidoc -o sphinx/modules src/absp --separate --force
sphinx-build -W --keep-going -b html sphinx docs/documentation


echo "=== Local CI completed successfully ==="
echo "    Unit tests      : reports/unit-tests.html"
echo "    Integration tests  : reports/integration-tests.html"
echo "    Code coverage   : reports/coverage/index.html"
echo "    Security tests    : reports/security_report.html"
echo "    Documentation      : docs/documentation/index.html"