import threading


class RequestCounterMiddleware:
    _request_count_lock = threading.Lock()
    _request_count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with self._request_count_lock:
            RequestCounterMiddleware._request_count += 1

        response = self.get_response(request)
        return response