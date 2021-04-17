from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'user_input_home'),
    path('fetch_data', views.fetch_data, name = 'fetched_data')
]
