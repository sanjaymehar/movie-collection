from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from task.middleware import RequestCounterMiddleware
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class RequestCountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with RequestCounterMiddleware._request_count_lock:
            count = RequestCounterMiddleware._request_count
        return Response({'requests': count})


@method_decorator(csrf_exempt, name='dispatch')
class ResetRequestCountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        with RequestCounterMiddleware._request_count_lock:
            RequestCounterMiddleware._request_count = 0
        return Response({'message': 'Request count reset successfully'})