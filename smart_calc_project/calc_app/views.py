from .logic import Logic, FinalOffer, FillerInfo
from .models import Equipment, Filler
from django import forms

from django.shortcuts import render
from .forms import FlatForm, CountryHouseForm, HouseForm, OutputForm
from django.views import View

class FullFiller:
    def __init__(self, id, name, necessery_v, stocks_v, price) -> None:
        self.id = id
        self.name = name
        self.necessery_v = necessery_v
        self.stocks_v = stocks_v
        self.price = price

class FullOffer:
    def __init__(self, ids_offer:FinalOffer ) -> None:
        self.main_filters = [Equipment.objects.get(equipment_id=main_id) for main_id in ids_offer.main_equipments]
        self.kitchen_filters = [Equipment.objects.get(equipment_id=kitchens_filter_id) for kitchens_filter_id in ids_offer.kitchen_filters]
        __res = [self.__get_filler_info(filler) for filler in ids_offer.fillers]

        self.fillers = [FullFiller(r[0],r[1],r[2],r[3],r[4]) for r in __res]

        self.extra_equipmets = ids_offer.extra_offers

    def __get_filler_info(self, filler: FillerInfo):
        filler_row = Filler.objects.get(filler_id=filler.id)
        print(f'на возврат\n{(filler_row.filler_id, filler_row.filler_name, filler.v, filler_row.filler_v, filler.price)}')
        return filler_row.filler_id, filler_row.filler_name, filler.v, filler_row.filler_v, filler.price
    def __str__(self) -> str:
        return f'main: {self.main_filters}\nkitchen: {self.kitchen_filters}\nfillers: {self.fillers}\nextra: {self.extra_equipmets}'
class CalculataroView(View):
    template_name = 'calc_app/calc_page.html'
    people_num = 1
    flat_form = FlatForm()
    country_house_form = CountryHouseForm()
    house_form = HouseForm()
    
    main_filters_list = []
    kitchen_filters_list = []
    fillers_list = []
    #убрать необходимость отправлять в шаблон пустые списки
    context = {
        'flat_form': flat_form,
        'country_house_form': country_house_form,
        'house_form': house_form,
        'main_filters': main_filters_list,
        'kitchen_filters': kitchen_filters_list, 
        'fillers': fillers_list,
    }
    def __get_sumbitted_form(self, name_form, post_data):
        if name_form == 'flat_form':
            return FlatForm(post_data)
        if name_form == 'country_house_form':
            return CountryHouseForm(post_data)
        if name_form == 'house_form':
            return HouseForm(post_data)

    def get(self, request):
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request):

        name_form = request.POST.get('action')
        submitted_form = self.__get_sumbitted_form(name_form,request.POST)

        if submitted_form.is_valid():
            self.context[name_form]=submitted_form

            form_data = submitted_form.cleaned_data

            logic = Logic()
            print(form_data)
            if form_data['action'] == 'house_form' or form_data['action'] == 'country_form':
                ids_offer = logic.get_offers_ids(
                    water_hard=form_data['water_hardness'],
                    water_ferum=form_data['water_iron'],
                    name_form=form_data['action'],
                    people_num=form_data['people_number'],
                    smell=form_data['water_smell'],
                    extra_water_parametrs={
                        'water_turbidity': form_data['water_turbidity'], 
                        'water_PH': form_data['water_PH'], 
                        'water_oxid': form_data['water_oxid'], 
                        'water_nitrat': form_data['water_nitrat'], 
                        'water_salt': form_data['water_salt'], 
                        'water_nitrit': form_data['water_nitrit'], 
                        'water_color': form_data['water_color']
                    }
                )
            else:
                ids_offer = logic.get_offers_ids(
                    water_hard=form_data['water_hardness'],
                    water_ferum=form_data['water_iron'],
                    name_form=form_data['action'],
                    smell=form_data['water_smell'],
                    extra_water_parametrs={
                        'water_turbidity': form_data['water_turbidity'], 
                        'water_PH': form_data['water_PH'], 
                        'water_oxid': form_data['water_oxid'], 
                        'water_nitrat': form_data['water_nitrat'], 
                        'water_salt': form_data['water_salt'], 
                        'water_nitrit': form_data['water_nitrit'], 
                        'water_color': form_data['water_color']
                    }
                )
            offer = FullOffer(ids_offer)
            print(f'returned:{FullOffer(ids_offer)}')
            output = OutputForm(offer.main_filters, offer.kitchen_filters, offer.fillers)
            print(output.fillers_tr)
            self.context['output_form'] = output
            return render(request, template_name=self.template_name, context=self.context)

# Create your views here.
def calc_page(request):
    form_dict = {
    'flat_form':WaterForm,
    'country_form':ContryForm,
    'house_form':HouseForm,
    'output_form': OutputForm
    }
    people_num = 1

    flat_form = WaterForm()
    country_form = ContryForm()
    house_form = HouseForm()
    
    print('method ',request.method)
    main_filter_list = []
    kitchen_filter_list = []
    filler_list = []

    context = {
        'flat_form': flat_form,
        'country_form': country_form,
        'house_form': house_form,
        'main_filters': main_filter_list, 
        'kitchen_filters': kitchen_filter_list, 
        'fillers': filler_list,
        'test': forms.CharField(max_length=20)}

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
                        
            print(main_filter_list,'\n',kitchen_filter_list,'\n',filler_list)
            if name_form != 'output_form':
                out = OutputForm(main_filter_list, kitchen_filter_list, filler_list)
            else:
                out = OutputForm(request.POST)
            context['output_form']= out
    return render(request, 'calc_app/calc_page.html',context=context)