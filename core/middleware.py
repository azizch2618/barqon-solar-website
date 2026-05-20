import logging

from django.db import OperationalError, connections, close_old_connections
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger("barqon")


class DatabaseStabilityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        close_old_connections()
        try:
            response = self.get_response(request)
        except OperationalError as exc:
            connections.close_all()
            logger.exception("Database OperationalError on %s %s", request.method, request.path)
            if request.path.startswith("/api/"):
                return JsonResponse(
                    {
                        "detail": "Database is temporarily busy. Please retry in a few seconds.",
                        "retryable": True,
                        "error_code": "database_busy",
                    },
                    status=503,
                )
            return render(request, "500.html", {"error": exc}, status=500)
        finally:
            close_old_connections()
        return response
