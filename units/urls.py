from django.urls import path, include
from . import views

urlpatterns = [
    path('<unitname>/', views.unit_profile, name="unit_profile"),
]