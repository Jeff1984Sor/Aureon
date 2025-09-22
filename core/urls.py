from django.urls import path
from .views import HomeView

urlpatterns = [
    # A URL vazia ('') dentro do app core aponta para a HomeView.
    path('', HomeView.as_view(), name='home'),
]