from django.urls import path, include
from . import views

urlpatterns = [
    path('<username>/', views.profile, name="profile"),
]