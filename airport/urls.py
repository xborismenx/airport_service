from rest_framework.routers import DefaultRouter
from django.urls import path, include

from airport import views

router = DefaultRouter()
router.register('airports', views.AirportViewSet)
router.register("routes", views.RouteViewSet)
router.register("airplane_types", views.AirplaneTypeViewSet)
router.register("airplanes", views.AirplaneViewSet)
router.register("orders", views.OrderViewSet)
router.register("tickets", views.TicketViewSet)
router.register("flights", views.FlightViewSet)
router.register("crews", views.CrewViewSet)
urlpatterns = [
    path("", include(router.urls)),
]

app_name = 'airport'
