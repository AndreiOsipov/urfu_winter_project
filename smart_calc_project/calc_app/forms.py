from django import forms
from calc_app.models import Equipment

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class WaterForm(forms.Form):
    water_hardness = forms.FloatField(min_value=0, max_value=9, step_size=0.1, initial=0.0)
    water_iron = forms.FloatField(min_value=0, max_value=9, step_size=0.1, initial=0.0)
    water_turbidity = forms.FloatField(min_value=0, max_value=9, step_size=0.1, initial=0.0)
    water_PH = forms.FloatField(min_value=0, max_value=9, step_size=0.1, initial=0.0)
    water_oxid = forms.FloatField(min_value=0, max_value=9, step_size=0.1, initial=0.0)
    water_nitrat = forms.FloatField(min_value=0, max_value=9, step_size=0.1, initial=0.0)
    water_salt = forms.FloatField(min_value=0, max_value=9, step_size=0.1, initial=0.0)
    water_nitrit = forms.FloatField(min_value=0, max_value=9, step_size=0.1, initial=0.0)
    water_color = forms.FloatField(min_value=0, max_value=9, step_size=0.1, initial=0.0)
    water_smell = forms.NullBooleanField(widget=forms.RadioSelect(
        choices=[
            (True, 'Да'),
            (False, 'Нет'),
        ]
    ), initial = False)

class FlatForm(WaterForm):
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='flat_form')
class HouseForm(WaterForm):
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='house_form')
    people_number = forms.IntegerField(min_value=1, initial=1)

class CountryHouseForm(WaterForm):
    action = forms.CharField(max_length=20, widget=forms.HiddenInput(), initial='country_house_form')
    people_number = forms.IntegerField(min_value=1, initial=1)


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
        #тут придется работать с сессиями
        
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