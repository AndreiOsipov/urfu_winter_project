from django.urls import path
from . import views

app_name  = 'calc_app' #разобраться с настройкой URL

urlpatterns = [
    path('', views.calc_page, name='calc_page'),
]