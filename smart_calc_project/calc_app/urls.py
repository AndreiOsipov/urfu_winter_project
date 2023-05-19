from django.urls import path
from django.urls import path, register_converter
from . import views

app_name  = 'calc_app'
#переделать url:
#сделать так, чтобы url с кадой формы передавался с уникальным аргументом <>
class FloatConverter:
    regex = "[0-9]+.[0-9]+"
    
    def to_python(self, str_value):
        return float(str_value)

    def to_url(self, value):
        return str(value)

class BoolConverter:
    regex = "[A-Z][a-z]"

    def to_python(self, str_value):
        return str_value=='True'
    
    def to_url(self, value):
        return str(value)

register_converter(FloatConverter, 'float')
register_converter(BoolConverter, 'bool')

urlpatterns = [
    path('', views.GetSearcheForm.as_view(), name='calc_page'),
    path('get_complect/',views.GetComplectView.as_view(), name = 'retrived_complect'),
    path('get_contract/',views.GetContractView.as_view(), name = 'get_contract'),
]