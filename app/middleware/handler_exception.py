from typing import Any

from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response

from app.layer.constants import EXCEPTIONS_HANDLING_MIDDLEWARE


class HandleException:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request) -> Response:
        return self.get_response(request)

    def process_exception(self, request: Request, exception: Any):
        if isinstance(exception, EXCEPTIONS_HANDLING_MIDDLEWARE):
            return JsonResponse({"error": str(exception)}, status=exception.code)

        return None
