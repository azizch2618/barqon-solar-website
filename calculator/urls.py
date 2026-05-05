from django.urls import path

from .views import calculate_load, calculation_history

urlpatterns = [
    path("calculate/", calculate_load, name="calculate-load"),
    path("history/", calculation_history, name="calculation-history"),
]
