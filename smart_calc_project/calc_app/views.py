from .models import Equipment, EquipmentType
from django import forms
from .forms import (NumberFlatForm, 
    NumberCountryHouseForm, 
    NumberHouseForm,
    BoolFlatForm,
    BoolCountryHouseForm,
    BoolBaseHouseForm,
    ExcelForm)

from .parser import ExcelParser, ExcelEquipment

from django.shortcuts import render
from django.views import View

class CalculatorView(View):
    template_name = 'calc_app/calc_page.html'
    people_num = 1
    flat_form = NumberFlatForm()
    country_house_form = NumberCountryHouseForm()
    house_form = NumberHouseForm()
    bool_flat_form = BoolFlatForm()
    bool_country_house_form = BoolCountryHouseForm()
    bool_house_form = BoolBaseHouseForm()

    excel_form = ExcelForm()

    #TODO make the  output form
    main_filters_list = []
    kitchen_filters_list = []
    fillers_list = []
    
    context = {
        'flat_form': flat_form,
        'country_form': country_house_form,
        'house_form': house_form,
        'bool_flat_form': bool_flat_form,
        'bool_country_form':bool_country_house_form,
        'bool_house_form':bool_house_form,
        'excel_form': excel_form,
        'main_filters': main_filters_list,
        'kitchen_filters': kitchen_filters_list, 
        'fillers': fillers_list,
        'not_saved_equipment': [],
    }

    def __get_sumbitted_form(self, name_form, post_data):
        print(f'post data: {post_data}')
        if name_form == NumberFlatForm().fields['action'].initial:
            return NumberFlatForm(post_data)
        if name_form == NumberCountryHouseForm().fields['action'].initial:
            return NumberCountryHouseForm(post_data)
        if name_form == NumberHouseForm().fields['action'].initial:
            return NumberHouseForm(post_data)
        if name_form == BoolFlatForm().fields['action'].initial:
            return BoolFlatForm(post_data)
        if name_form == BoolCountryHouseForm().fields['action'].initial:
            return BoolCountryHouseForm(post_data)
        if name_form == BoolBaseHouseForm().fields['action'].initial:
            return BoolBaseHouseForm(post_data)
    
    def __search_configuration(self, model, search_parametrs):
        queryset = model.all()
        if 'people_num' in search_parametrs.keys():
            queryset = queryset.filter(people_num = 'people_num')
        if search_parametrs['water_smell'] == True:
            return queryset.get(water_smell = True)

        if 'water_npc' in search_parametrs.keys():
            if search_parametrs['water_npc'] == True:
                return queryset.get(water_npc = True)
            queryset = queryset.filter(
                water_hardness = search_parametrs['water_hardness'], 
                water_ferum = search_parametrs['water_ferum'],
                water_mpc = False,
                water_smell = False,)
                
    def get(self, request):
        name_form = request.GET.get('action')
        search_form = self.__get_sumbitted_form(name_form, request.GET)
        if search_form.is_valid():
            search_parametrs = search_form.data
            model = search_form.Meta.model
            configuration = self.__search_configuration(search_parametrs)

        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request):

        name_form = request.POST.get('action')
        
        submitted_form = self.__get_sumbitted_form(name_form,request.POST)
        self.context[name_form]=submitted_form
        if submitted_form.is_valid():
            form_data = submitted_form.cleaned_data

            if name_form == 'excel_form':
                uploaded_file = form_data['input_excel']
                parser = ExcelParser()
                equipment_list = parser.generate_equipment_list(uploaded_file)
                for excel_equipment in equipment_list:
                    try:
                        equipment_type, was_created = EquipmentType.objects.get_or_create(type_name = excel_equipment.name, type_discount = 0)
                        Equipment.objects.update_or_create(
                            equipment_name = excel_equipment.name,
                            equipment_price = excel_equipment.price,
                            equipment_id = excel_equipment.id,
                            equipment_type = equipment_type)
                    except:
                        self.context['not_saved_equipment'].append(excel_equipment.name)
            else:
                print(submitted_form)
                model_for_input_data = self.get_model(form_data)
                water_data_object = self.__get_water_data_object(form_data)
                #equipment_list = Equipment.objects.get()
        print(submitted_form.errors)
        return render(request, template_name=self.template_name, context=self.context)