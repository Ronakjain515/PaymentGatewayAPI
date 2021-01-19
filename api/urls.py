from django.urls import path
from .views import ProcessPayment

urlpatterns = [
    path('ProcessPayment', ProcessPayment.as_view()),
]
