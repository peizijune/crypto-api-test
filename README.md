### API Automation Testing Framework (Python + Pytest + Behave + Playwright + Allure)

This repository provides a lightweight, production-ready framework for API automation testing that supports:

- **REST API** testing (using Python Playwright `APIRequestContext)`
- **WebSocket** testing (using `websocket-client`)
- **Two test runners**: Pytest and Behave (BDD)
- **Data-driven** tests via JSON files
- **Environment-based config** (UAT, PROD) with a single switch
- **Allure** reporting with environment details

Demo targets (UAT):

- REST: `https://uat-api.3ona.co/exchange/v1/public/get-candlestick?instrument_name=BTCUSD-PERP`
- WebSocket (Market Data): `wss://uat-stream.3ona.co/exchange/v1/market` (demo subscribes to `book.BTCUSD-PERP.10`)
- WebSocket (User API): `wss://uat-stream.3ona.co/exchange/v1/user` (not used in demo)

---

## 1) Prerequisites / Environment Setup

- Python 3.10+ (recommended 3.11)
- Node is NOT required (we use Python Playwright)
- Allure CLI for report viewing (Java required)

Steps:

1. Create and activate a virtual environment (macOS):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```bash
   python -m playwright install
   ```
4. Install Allure CLI (choose one):
   - macOS (brew):
     ```bash
     brew install allure
     ```
   - Manual: download from `https://github.com/allure-framework/allure2/releases` and add to PATH.

Optional environment variables:

- `TEST_ENV` selects environment (`UAT` or `PROD`). Default: `UAT`
- `ALLURE_RESULTS_DIR` sets allure results directory. Default: `allure-results`

---

## 2) Project Structure

```



crypto-api-test/
  behave.ini
  pytest.ini
  requirements.txt
  config/
    env.json                # UAT/PROD endpoints
  data/
    rest/                   # Data sets for REST tests
      public-get-candlestick.json  
    ws/
      market/               # Message for WebSocket (Market Data Subscriptions)
        book-instrument_name-depth.json
      user/                 # Message for WebSocket (User API and Subscriptions)   
  scripts/
    run_pytest.sh           # Run pytest and write Allure results
    run_behave.sh           # Run behave and write Allure results
  tests/
    pytest/
      conftest.py           # Fixtures: env config, Playwright APIRequestContext, Allure env writer
      test_rest_public.py   # REST demo (data-driven)
      test_ws_market.py     # WebSocket demo (subscribe)
    behave/
      features/
        environment.py      # Env + Playwright setup, Allure env writer
        rest_candlestick.feature
        ws_subscribe.feature
      steps/
        rest_steps.py
        ws_steps.py
  utils/
    allure_env.py           # Writes environment.properties for Allure
    config.py               # Loads env config and Allure results dir
    data_loader.py          # JSON loader helper
```

---

## 3) How environment config works

- Configuration is stored in `config/env.json`.
- Select environment via:
  - Env var: `TEST_ENV=UAT` or `TEST_ENV=PROD`
  - Pytest CLI: `--env UAT`
  - Behave CLI: `-D env=UAT`
- Allure environment info is written to `allure-results/environment.properties` automatically by both runners.

`config/env.json` example keys:

- `rest_base_url`: base URL for REST requests
- `ws_market_url`: WebSocket endpoint for market data
- `ws_user_url`: WebSocket endpoint for user/private data

---

## 4) Running the tests

Pytest (default UAT):

```bash
./scripts/run_pytest.sh
```

Pytest (explicit env):

```bash
TEST_ENV=UAT ./scripts/run_pytest.sh
# or
./scripts/run_pytest.sh --env UAT
```

Run only WebSocket tests:

```bash
./scripts/run_pytest.sh -m ws
```

Behave (default UAT):

```bash
./scripts/run_behave.sh
```

Behave (explicit env):

```bash
./scripts/run_behave.sh -D env=UAT
```

Open Allure report:

```bash
allure serve allure-results
```

---

## 5) Writing new tests

### 5.1 Pytest (REST)

1. Add a new JSON dataset under `data/rest/`:
   ```json
   [
     {
       "name": "BTCUSD-PERP 1m candlestick",
       "path": "/exchange/v1/public/get-candlestick",
       "params": { "instrument_name": "BTCUSD-PERP", "timeframe": "1m", "count": 5 }
     }
   ]
   ```
2. Parametrize in a test using `load_json_file(...)`:
   ```python

   ```

  @pytest.mark.parametrize("case", load_json_file(Path("data/rest/public-get-candlestick.json")))
   def test_something(api_context: APIRequestContext, case: dict):
       resp = api_context.get(case["path"], params=case["params"])
       assert resp.ok

```

### 5.2 Pytest (WebSocket)

- Use `websocket-client` to connect, send messages from data files, and assert responses.
- Example in `tests/pytest/test_ws_market.py`.

### 5.3 Behave (BDD)

- Add a `.feature` file in `tests/behave/features/`.
- Implement step definitions under `tests/behave/steps/`.
- `environment.py` initializes Playwright request context and writes Allure env info.

---

## 6) Debugging tips

- Print response text on failure: Pytest already asserts with body content in `test_rest_public.py`.
- Increase WebSocket timeouts if network is slow (see helper in tests).
- Run a single Pytest test:
  ```bash
  ./scripts/run_pytest.sh -k test_get_candlestick_success -vv
```

- Run a single Behave scenario:
  ```bash
  ./scripts/run_behave.sh --name "Get BTCUSD-PERP candlestick successfully"
  ```

---

## 7) Notes

- Playwright is used for REST API testing via `APIRequestContext`.
- WebSocket is implemented with `websocket-client` for simplicity and reliability in headless test environments.
- Allure shows environment details (Environment, REST Base URL, WS Market URL, WS User URL) in the report sidebar.
- For Production REST requests, an API key is required. Provide it via `API_KEY` environment variable or in `config/env.json` under the `PROD` section; the framework sends it as `api_key` header automatically.
- All numeric values in request payloads must be strings (e.g., `"5"`, `"12.34"`). Demo WebSocket subscription uses `"id": "1"` accordingly.
