from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ElevatorViewSet, call_elevator, step,
                    open_door, close_door, elevator_control_panel,
                    choose_target_floor)

router = DefaultRouter()
router.register(r'elevator', ElevatorViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/call-elevator/', call_elevator, name="call_elevator"),
    path('api/step/', step),
    path('api/open/', open_door),
    path('api/close/', close_door),
    path('api/choose-target-floor', choose_target_floor, name="choose_target_floor"),
    path('view/', elevator_control_panel, name="elevator_control_panel"),

]