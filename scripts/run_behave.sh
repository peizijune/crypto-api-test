#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   TEST_ENV=UAT ./scripts/run_behave.sh
#   ./scripts/run_behave.sh -D env=UAT

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export TEST_ENV="${TEST_ENV:-UAT}"
export ALLURE_RESULTS_DIR="${ALLURE_RESULTS_DIR:-allure-results}"

behave -D env="${TEST_ENV}" -f allure_behave.formatter:AllureFormatter -o "${ALLURE_RESULTS_DIR}"
echo "Allure results written to: ${ALLURE_RESULTS_DIR}"
echo "Generate and serve report with:"
echo "  allure serve ${ALLURE_RESULTS_DIR}"

