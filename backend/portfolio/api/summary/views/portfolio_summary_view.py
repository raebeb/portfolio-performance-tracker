from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from ....models import Portfolio
from ....services.calculations import calculate_daily_values
from ..serializers.portfolio_summary_serializer import PortfolioSummarySerializer

class PortfolioSummaryView(APIView):


    def get(self, request, portfolio_id):
        fecha_inicio = request.GET.get("fecha_inicio")
        fecha_fin = request.GET.get("fecha_fin")

        if not fecha_inicio or not fecha_fin:
            return Response(
                {"error": "Parámetros fecha_inicio y fecha_fin son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Formato de fecha inválido. Usa YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        portfolio = get_object_or_404(Portfolio, pk=portfolio_id)

        data = calculate_daily_values(portfolio, fecha_inicio, fecha_fin)
        def round_value(value, decimal_places=2):
            return Decimal(value).quantize(Decimal(10) ** -decimal_places, rounding=ROUND_HALF_UP)

        serialized_data = []
        for fecha, contenido in data.items():
            serialized_data.append({
                "date": fecha,
                "total_value": round_value(contenido["total_value"]),
                "weights": {k: round_value(v["weight"]) for k, v in contenido["assets"].items()}
            })

        serializer = PortfolioSummarySerializer(data=serialized_data, many=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

