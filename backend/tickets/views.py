from django.db.models import Count, Avg
from django.db.models.functions import TruncDate

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Ticket
from .serializers import TicketSerializer

from rest_framework.views import APIView
from .llm import classify_description



class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]

    filterset_fields = ["category", "priority", "status"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        # 1) Total tickets
        total_tickets = Ticket.objects.count()

        # 2) Open tickets
        open_tickets = Ticket.objects.filter(status=Ticket.Status.OPEN).count()

        # 3) Avg tickets per day (ORM only)
        per_day = (
            Ticket.objects.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
        )

        avg_tickets_per_day = per_day.aggregate(avg=Avg("count"))["avg"] or 0

        # 4) Priority breakdown (ORM only)
        priority_breakdown = (
            Ticket.objects.values("priority")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # 5) Category breakdown (ORM only)
        category_breakdown = (
            Ticket.objects.values("category")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return Response(
            {
                "total_tickets": total_tickets,
                "open_tickets": open_tickets,
                "avg_tickets_per_day": round(float(avg_tickets_per_day), 2),
                "priority_breakdown": list(priority_breakdown),
                "category_breakdown": list(category_breakdown),
            }
        )

class TicketClassifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        description = request.data.get("description", "")

        if not description or not isinstance(description, str):
            return Response(
                {"detail": "description is required"},
                status=400
            )

        result = classify_description(description)
        return Response(result, status=200)
