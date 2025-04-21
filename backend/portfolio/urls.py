from django.urls import path
from .api.summary.views.portfolio_summary_view import PortfolioSummaryView

urlpatterns = [
    path('api/portfolios/<int:portfolio_id>/summary/', PortfolioSummaryView.as_view(), name='portfolio-summary'),
]
