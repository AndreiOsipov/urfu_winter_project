from django.urls import path
from . import views

app_name  = 'calc_app'
#переделать url:
#сделать так, чтобы url с кадой формы передавался с уникальным аргументом <>

urlpatterns = [
    path('', views.CalculatorView.as_view(), name='calc_page'),
]