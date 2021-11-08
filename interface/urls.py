from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('data/', views.data, name="data"),
    path('map/', views.unit_map, name="map"),
    # path('notices/', views.notices, name="notices"),
    # path('contact/', views.contact, name="contact"),
    # path('notices/add_notice', views.add_notice, name="add_notice"),
    # path('notices/<id>', views.notice_detail, name="notice_detail"),
    # path('notices/<id>/delete', views.delete_notice, name="delete"),
    # path('notices/<id>/edit_notice', views.edit_notice, name="edit"), # why does this load the add notice template (but still work?)
    # path('profile/', include('users.urls'))
]