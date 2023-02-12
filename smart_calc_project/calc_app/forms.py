import os
from django.core.exceptions import ValidationError
from django import forms
from calc_app.models import Equipment

class ExcelFileInputFiled(forms.FileField):
    def validate(self, file):
        """Check if file format is not sucess."""
        super().validate(file)
        ext = os.path.splitext(file.name)[1]
        if ext not in ['.xls', '.xlsx']:
            self.error_messages = 'wrong format'
            raise ValidationError(message = 'wrong format',code='format_error')
            
class AbstractWaterForm(forms.Form):
    water_smell = forms.NullBooleanField(widget=forms.RadioSelect(choices=[(True, 'да'), (False, 'Нет')]),initial=False,label='запах')
    field_order = ['people_number',]

class NumberWaterForm(AbstractWaterForm):
    water_hardness = forms.ChoiceField(choices=[(0, 'до 3'),(3, 'до 8'),(8, 'до 15'), (20, 'от 15')],initial=False,label='жесткость')
    water_iron = forms.ChoiceField(choices=[(0, 'до 0,3'), (0.3, 'до 0,9'), (0.9, 'до 8'), (8, 'от 8')],initial=False,label='железо')
    water_turbidity = forms.NullBooleanField(widget=forms.RadioSelect(choices=[(True, 'да'), (False, 'Нет')]),initial=False,label='мутность')
    water_PH = forms.NullBooleanField(widget=forms.RadioSelect(choices=[(True, 'да'), (False, 'Нет')]),initial=False,label='Ph')
    water_oxid = forms.NullBooleanField(widget=forms.RadioSelect(choices=[(True, 'да'), (False, 'Нет')]),initial=False,label='оксиды')
    water_nitrat = forms.NullBooleanField(widget=forms.RadioSelect(choices=[(True, 'да'), (False, 'Нет')]),initial=False,label='нитраты')
    water_salt = forms.NullBooleanField(widget=forms.RadioSelect(choices=[(True, 'да'), (False, 'Нет')]),initial=False,label='солесодержание')
    water_nitrit = forms.NullBooleanField(widget=forms.RadioSelect(choices=[(True, 'да'), (False, 'Нет')]),initial=False,label='нитриты')
    water_color = forms.NullBooleanField(widget=forms.RadioSelect(choices=[(True, 'да'), (False, 'Нет')]),initial=False,label='цветность')

class BoolWaterForm(AbstractWaterForm):
    water_hardness = forms.BooleanField()
    water_iron = forms.BooleanField()
    
class NumberFlatForm(NumberWaterForm):
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='flat_form')
    
class NumberHouseForm(NumberWaterForm):
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='house_form')
    people_number = forms.IntegerField(min_value=1, initial=1, label='количество человек')

class NumberCountryHouseForm(NumberWaterForm):
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='country_house_form')
    people_number = forms.IntegerField(min_value=1, initial=1, label='количество человек')


class BoolFlatForm(BoolWaterForm):
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='bool_flat_form')
    
class BoolCountryHouseForm(BoolWaterForm):
    people_number = forms.IntegerField(min_value=1, initial=1, label='количество человек')
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='bool_country_house_form')


class BoolBaseHouseForm(BoolWaterForm):
    people_number = forms.IntegerField(min_value=1, initial=1)
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='bool_base_house_form')


class ExcelForm(forms.Form):
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='excel_form')
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
        
class FillerTr:
    '''
    поля формы нааполнлителя
    '''
    def __init__(self, filler_name, filler_price, necessary_v, stock_v) -> None:
        self.name = filler_name
        self.price = filler_price
        self.necessary_v = necessary_v
        self.stock_v = stock_v
    def update(self, data):
        #тут придется работать с сессиями
        self.name_nput = forms.CharField(max_length=20, initial=data)
        #self.price_input = forms.DecimalField(initial=Equipment.objects.get(filler_name=data).price)
        

class OutputForm(forms.Form):
    '''
    переопределен метод __init__
    создает форму на основе данных из трех списков
    self.fields[f'main_component_{i}_name']  -- таким образом устанавливается атрибут в цикле
    тремя циклами он запихивает элементы из списков в свои атрибуты, 
    и в списки из которых эти поля рендерятся в шаблоне

    '''
    equipments_relations = {forms.CharField :forms.DecimalField}#пока ненужно
    main_filters_tr = []
    kitchen_filters_tr = []
    fillers_tr = []
    
    name_tr_dict = {}

    def __init__(self, main_components: list[Equipment], kitchen_filters: list[Equipment], fillers_with_v, *args, **kwargs):

        super(OutputForm, self).__init__(*args, **kwargs)

        self.main_filters_tr = []
        self.kitchen_filters_tr = []
        self.fillers_tr = []

        for i in range(len(main_components)):
            #для каждого оборудования из списка создаются поля названия, цены, количества
            self.fields[f'main_component_{i}_name'] = forms.ChoiceField(choices=[(eq.equipment_id, eq.name) for eq in Equipment.objects.all()], initial=(main_components[i].equipment_id,main_components[i].name))
            self.fields[f'main_component_{i}_price'] = forms.DecimalField(initial=main_components[i].price)     
            filter_tr = FilterTr(
                self[f'main_component_{i}_name'],  #почему-то django не может просто так работать с полями, если они в 
                self[f'main_component_{i}_price'], #списках или упрятаны в другие классы, поэтому тут так. я пока сам не понял до конца как это
                main_components[i].number)          #работает, но похоже, что так в класс улетает не только поле ввода, но и форма к которой она принадлежит
            self.main_filters_tr.append(filter_tr)
        #кухонный фильтр нужен только один, поэтому без циклов(все фильтры из kitchen_filters упаковываются в один ChoisesFiled)
        if len(kitchen_filters)>0:
            self.fields[f'kitchen_filters_name'] = forms.ChoiceField(choices=[(kitchen_f.equipment_id,kitchen_f.name) for kitchen_f in kitchen_filters], initial=(kitchen_filters[0].equipment_id,kitchen_filters[0].name))
            self.fields[f'kitchen_filters_price'] = forms.DecimalField(initial=kitchen_filters[0].price)
            filter_tr = FilterTr(
                    self[f'kitchen_filters_name'],
                    self[f'kitchen_filters_price'],
                    kitchen_filters[0].number)
            self.kitchen_filters_tr.append(filter_tr)
        
        for i in range(len(fillers_with_v)):
            self.fields[f'filler_{i}_name'] = forms.ChoiceField(choices = [(filler.id,filler.name) for filler in fillers_with_v], initial=(fillers_with_v[i].id, fillers_with_v[i].name))
            self.fields[f'filler_{i}_price'] = forms.DecimalField(initial=fillers_with_v[i].price)
            filler_tr = FillerTr(
                self[f'filler_{i}_name'],
                self[f'filler_{i}_price'],
                fillers_with_v[i].necessery_v,
                fillers_with_v[i].stocks_v)
            self.fillers_tr.append(filler_tr)
            print('\n\nвсе добавлено\n\n',len(self.fillers_tr))
    '''
    def set_new_values(self, form_data_dict):
        for key in form_data_dict.keys():
            if key in self.name_tr_dict.keys():
                self.name_tr_dict[key].update(form_data_dict[key])
    '''