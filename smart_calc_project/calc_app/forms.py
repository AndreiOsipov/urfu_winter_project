import os
from django.core.exceptions import ValidationError
from django import forms
from django.db.models import QuerySet
from calc_app.models import (
    Equipment,
    FlatHouseWithWaterAnalysis, 
    FlatHouseWithoutWaterAnalysis, 
    CountryHouseWithWaterAnalysis,
    CountryHouseWithoutWaterAnalysis,
    BaseHouseWithWaterAnalysis,
    BaseHouseWithoutWaterAnalysis,
    )

class ExcelFileInputFiled(forms.FileField):
    def validate(self, file):
        """Check if file format is not sucess."""
        super().validate(file)
        ext = os.path.splitext(file.name)[1]
        if ext not in ['.xls', '.xlsx']:
            self.error_messages = 'wrong format'
            raise ValidationError(message = 'wrong format',code='format_error')

class FloatChoiceField(forms.ChoiceField):
    def to_python(self, value):
        return float(super().to_python(value))

class NumberFlatForm(forms.Form):

    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), initial='flat_form')
    water_hardness = FloatChoiceField(choices=[(0, 'до 3'), (3, 'до 7'), (7, 'от 7')], label='жесткость')
    water_ferum = FloatChoiceField(choices=[(0, 'до 0,6'),(0.6, 'до 0,9'), (0.9, 'от 0,9')], label='железо')
    water_mpc = forms.BooleanField(label='Другие примеси', required=False)

    class Meta:
        model = FlatHouseWithWaterAnalysis
        fields = [
        'water_hardness',
        'water_ferum',
        'water_mpc',
    ]

class NumberCountryHouseForm(forms.Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), initial='country_house_form')
    water_v_used_per_hour = FloatChoiceField(
        choices=[
            (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), 
            (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)')],
        label='людей в доме')
    water_hardness = FloatChoiceField(
        choices=[
            (0, 'до 3'),
            (3, 'до 7'),
            (7, 'от 7')],
        label='жесткость')
    water_ferum = FloatChoiceField(
        choices=[
            (0, 'до 0,3'),
            (0.3, 'до 0,9'),
            (0.9, 'от 0,9')],
        label='железо')
    water_mpc = forms.BooleanField(label='другие примеси', required=False)
    water_smell = forms.BooleanField(label='запах', required=False)

    class Meta:
        model = CountryHouseWithWaterAnalysis
        fields = [
        'water_v_used_per_hour',
        'water_hardness',
        'water_ferum',
        'water_mpc',
        'water_smell',
    ]
        
class NumberHouseForm(forms.Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), initial='house_form')
    water_v_used_per_hour = FloatChoiceField(choices=[
            (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'),
            (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)'),
            (2.0, '5 - 8 человек (до 2,5-х куб.м./ч)'),
            (2.5, '8 и более человек(от 2,5 - х куб.м./ч)')],
        label='людей в доме')
    water_hardness = FloatChoiceField(choices=[
            (0, 'до 3'),
            (3, 'до 8'),
            (8, 'до 15'),
            (20, 'от 15')], 
        label='жесткость')
    water_ferum = FloatChoiceField(choices=[
            (0, 'до 0,3'),
            (0.3, 'до 0,9'),
            (0.9, 'до 8'),
            (8, 'от 8')],
        label='железо')
    water_mpc = forms.BooleanField(label='другие примеси', required=False)
    water_smell = forms.BooleanField(label='запах', required=False)

    class Meta:
        model = BaseHouseWithWaterAnalysis
        fields = [
        'water_v_used_per_hour',
        'water_hardness',
        'water_ferum',
        'water_mpc',
        'water_smell',
    ]
    
class BoolFlatForm(forms.Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), initial='bool_flat_form')
    water_hardness = forms.BooleanField(label='жесткость', required=False)
    water_ferum = forms.BooleanField(label='железо', required=False)

    class Meta:
        model = FlatHouseWithoutWaterAnalysis
        fields = [
        'water_hardness',
        'water_ferum']

class BoolCountryHouseForm(forms.Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), initial='bool_country_house_form')
    water_v_used_per_hour = forms.ChoiceField(choices=[
            (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'),
            (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)')],
            label='лидей в доме')
    water_hardness = forms.BooleanField(label='жесткость', required=False)
    water_ferum = forms.BooleanField(label='железо', required=False, initial=False)
    water_smell = forms.BooleanField(label='запах', required=False, initial=False)
    
    class Meta:
        model = CountryHouseWithoutWaterAnalysis
        fields = [
        'water_v_used_per_hour',
        'water_hardness',
        'water_ferum',
        'water_smell',
    ]

class BoolBaseHouseForm(forms.Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), initial='bool_base_house_form')
    water_v_used_per_hour = forms.ChoiceField(choices=[
        (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'),
        (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)'),
        (2.0, '5 - 8 человек (до 2,5-х куб.м./ч)'),
        (2.5, '8 и более человек(от 2,5 - х куб.м./ч)')],
        label='людей в доме')
    water_hardness = forms.BooleanField(label='жесткость', required=False)
    water_ferum = forms.BooleanField(label='железо', required=False)
    water_smell = forms.BooleanField(label='запах', required=False)

    class Meta:
        model =  BaseHouseWithoutWaterAnalysis
        fields = [
        'water_v_used_per_hour',
        'water_hardness',
        'water_ferum',
        'water_smell',
    ]

class ExcelForm(forms.Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), initial='excel_form')
    input_excel = ExcelFileInputFiled(label='обновить данные excel-файлом')


class FilterTr:
    '''
    представляет поля формы фильтра для одной строки таблицы
    '''
    def __init__(self, filter_name, filter_price, stock_num) -> None:
        self.name_input = filter_name
        self.price_input = filter_price
        self.num = stock_num

    def update(self, data):
        self.name_input = forms.CharField(max_length=20, initial=data)
        self.price_input = forms.DecimalField(initial=Equipment.objects.get(name=data).price)

        
class EquipmentRow:
    '''
    нужен, имя и цену оборудования сгруппировать в одну строку
    '''
    def __init__(self, name_form, price_form) -> None:
        self.name_form = name_form
        self.price_form = price_form
        
class OutputForm(forms.Form):
    '''
    переопределен метод __init__
    создает форму на основе данных из трех списков
    self.fields[f'main_component_{i}_name']  -- таким образом устанавливается атрибут в цикле
    тремя циклами он запихивает элементы из списков в свои атрибуты, 
    и в списки из которых эти поля рендерятся в шаблоне
    '''
    def __generate_fields(self, equipment: Equipment):
        equipments_with_same_type = Equipment.objects.filter(equipment_type=equipment.equipment_type)
        
        self.fields[f'{equipment.equipment_name}_{self.last_field_number}'] = forms.ChoiceField(choices=
            list(map(lambda found_equipment: (found_equipment.equipment_name, found_equipment.equipment_name), 
            equipments_with_same_type)),
            initial = (equipment.equipment_name, equipment.equipment_name))
        self.fields[f'{equipment.equipment_name}_{self.last_field_number}_price'] = forms.FloatField(
            initial=equipment.equipment_price)
          
        self.rows_with_fields.append(EquipmentRow(
            self[f'{equipment.equipment_name}_{self.last_field_number}'],
            self[f'{equipment.equipment_name}_{self.last_field_number}_price']))
        
    def __init__(self, equipments: QuerySet, *args, **kwargs):
        self.last_field_number = 0
        self.rows_with_fields = []
        super(OutputForm, self).__init__(*args, **kwargs)
        for equipment in equipments:
            self.__generate_fields(equipment)
            self.last_field_number+=1