#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   TEST_ENV=UAT ./scripts/run_pytest.sh
#   ./scripts/run_pytest.sh --env UAT -k ws

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export TEST_ENV="${TEST_ENV:-UAT}"
export ALLURE_RESULTS_DIR="${ALLURE_RESULTS_DIR:-allure-results}"

python -m pytest "$@" --env "${TEST_ENV}" --alluredir "${ALLURE_RESULTS_DIR}"
echo "Allure results written to: ${ALLURE_RESULTS_DIR}"
echo "Generate and serve report with:"
echo "  allure serve ${ALLURE_RESULTS_DIR}"

