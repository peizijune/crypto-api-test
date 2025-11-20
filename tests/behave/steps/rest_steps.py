import json
from typing import Dict

from behave import given, when, then
from allure_commons._allure import attach
from allure_commons.types import AttachmentType


@given('I am using the "{env_name}" environment')
def step_set_env(context, env_name: str):
    # Already loaded in environment.py, but keep for readability
    assert context.cfg["name"].upper() == env_name.upper()


@when('I send GET "{path}" with query:')
def step_send_get_with_query(context, path: str):
    # Expect a 2-column table without headers: key | value
    params: Dict[str, str] = {row.cells[0]: row.cells[1] for row in context.table}

    response = context.api_context.get(path, params=params)
    context.response = response
    attach(json.dumps(params, indent=2), name="Request params", attachment_type=AttachmentType.JSON)
    attach(json.dumps(response.json(), indent=2), name="Response body", attachment_type=AttachmentType.JSON)


@then("the response status should be 200")
def step_status_ok(context):
    assert context.response.ok, f"Unexpected status {context.response.status}: {context.response.text()}"


@then("the response should contain any of the keys:")
def step_body_contains_any(context):
    body = context.response.json()
    keys = [row[0] for row in context.table]
    assert any(k in body for k in keys), f"None of {keys} present in response keys: {list(body.keys())}"

