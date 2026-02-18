# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import TicketViewSet, TicketClassifyView

# router = DefaultRouter()
# router.register(r"tickets", TicketViewSet, basename="tickets")

# urlpatterns = [
#     path("", include(router.urls)),

#     # LLM classify endpoint
#     path("tickets/classify/", TicketClassifyView.as_view(), name="ticket-classify"),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, TicketClassifyView

router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="tickets")

urlpatterns = [
    # IMPORTANT: Put classify BEFORE router.urls
    path("tickets/classify/", TicketClassifyView.as_view(), name="ticket-classify"),
    path("", include(router.urls)),
]
