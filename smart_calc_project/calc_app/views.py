from .logic import Logic
from .models import Equipment, Filler

from django.shortcuts import render
from .forms import WaterForm, ContryForm, HouseForm

class FullFiller:
    def __init__(self, id, name, necessery_v, stocks_v, price, ) -> None:
        self.id = id
        self.name = name
        self.necessery_v = necessery_v
        self.stocks_v = stocks_v
        self.price = price

# Create your views here.
def calc_page(request):
    form_dict = {
    'flat_form':WaterForm,
    'country_form':ContryForm,
    'house_form':HouseForm,
    }
    people_num = 1
    
    flat_form = WaterForm()
    country_form = ContryForm()
    house_form = HouseForm()
    
    print('method ',request.method)
    main_filter_list = []
    kitchen_filter_list = []
    filler_list = []


    if request.method == 'POST':
        name_form = request.POST.get('action')

        form = form_dict[name_form](request.POST)

        if name_form == 'flat_form':
            flat_form = form
        elif name_form == 'country_form':
            country_form = form
        elif name_form == 'house_form':
            house_form = form

        if form.is_valid():
            form_data = form.cleaned_data
            print(form_data)
            
            main_logic = Logic()
            if 'people_number' in form_data:
                people_num = form_data['people_number']
            logic_dict = main_logic.get_id_lists(form_data['water_iron'], form_data['water_hardness'],people_num, name_form) 
            
            for main_filter_id in logic_dict['main_filters_components']:
                main_filter_list.append(Equipment.objects.get(equipment_id = main_filter_id))
            
            if 'kitchen_filters' in logic_dict.keys():
                for kitchen_filter_id in logic_dict['kitchen_filters']:
                    kitchen_filter_list.append(Equipment.objects.get(equipment_id = kitchen_filter_id))
            
            if 'fillers' in logic_dict.keys():
                for filler in logic_dict['fillers']:
                    stocks_filler = Filler.objects.get(filler_id = filler.id)
                    filler_list.append(
                        FullFiller(
                            filler.id, stocks_filler.filler_name, filler.v, stocks_filler.filler_v, filler.price
                        ))
            print(
                main_filter_list,'\n',kitchen_filter_list,'\n',filler_list)
    return render(request, 'calc_app/calc_page.html', {
        'flat_form': flat_form,
        'country_form': country_form,
        'house_form': house_form,
        'main_filters': main_filter_list, 
        'kitchen_filters': kitchen_filter_list, 
        'fillers': filler_list})