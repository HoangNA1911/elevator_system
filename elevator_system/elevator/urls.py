from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ElevatorViewSet, call_elevator

router = DefaultRouter()
router.register(r'elevator', ElevatorViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('call-elevator/', call_elevator, name="call-elevator")
]