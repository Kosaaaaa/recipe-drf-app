"""
Core views for app.
"""
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from app.calc import factorial
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


@api_view(['GET'])
def health_check(request):
    """Returns successful response."""
    return Response({'healthy': True})


@api_view(['GET'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def factorial_view(request, n: int):
    return Response(data={'result': factorial(n)})
