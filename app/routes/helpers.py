import json
from typing import Any
from typing import Dict

from flask import request

from app.exceptions import BadRequest


def get_json() -> Dict[str, Any]:
    data = request.get_data()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        raise BadRequest
