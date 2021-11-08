from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('data/', views.data, name="data"),
    path('map/', views.unit_map, name="map"),
    # path('map/', views.UnitMapView.as_view(), name='map'),
]