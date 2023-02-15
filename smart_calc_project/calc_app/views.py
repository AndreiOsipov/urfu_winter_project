from .models import Equipment, EquipmentType
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from .forms import (NumberFlatForm, 
    NumberCountryHouseForm, 
    NumberHouseForm,
    BoolFlatForm,
    BoolCountryHouseForm,
    BoolBaseHouseForm,
    ExcelForm,
    OutputForm)

from .parser import ExcelParser

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

    def __get_sumbitted_form(self, name_form, post_data, files = None):
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
        if name_form == ExcelForm().fields['action'].initial:
            return ExcelForm(post_data, files)

    def __search_configuration(self, model, search_parametrs):
        queryset = model.objects.all()
        if 'water_v_used_per_hour' in search_parametrs.keys():
            queryset = queryset.filter(water_v_used_per_hour = search_parametrs['water_v_used_per_hour'])
        if 'water_smell' in search_parametrs.keys() and search_parametrs['water_smell'] == True:
            return queryset.get(water_smell = True).equipments.all()
        if 'water_mpc' in search_parametrs.keys() and search_parametrs['water_mpc'] == True:
            return queryset.get(water_mpc = True).equipments.all()
        return queryset.get(**search_parametrs).equipments.all()
            
    def get(self, request):
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request):

        name_form = request.POST.get('action')
        submitted_form = self.__get_sumbitted_form(name_form, request.POST, request.FILES)   
        self.context[name_form]=submitted_form
        if submitted_form.is_valid():
            form_data = submitted_form.cleaned_data
            if name_form == 'excel_form':
                uploaded_file = form_data['input_excel']
                parser = ExcelParser()
                equipment_list = parser.generate_equipment_list(uploaded_file)
                for excel_equipment in equipment_list:
                    try:
                        equipment_type, was_created = EquipmentType.objects.get_or_create(type_name = excel_equipment.type, type_discount = 0)
                        Equipment.objects.update_or_create(
                            equipment_name = excel_equipment.name,
                            equipment_price = excel_equipment.price,
                            equipment_id = excel_equipment.id,
                            equipment_type = equipment_type)
                    except:
                        self.context['not_saved_equipment'].append(excel_equipment.name)
            else:
                search_parametrs = {
                    parametr: submitted_form.cleaned_data[parametr]
                    for parametr in submitted_form.cleaned_data.keys() 
                    if parametr != 'action'}
                model = submitted_form.Meta.model
                configuration = self.__search_configuration(model, search_parametrs)
                output_form = OutputForm(configuration)
                self.context['output_form'] = output_form
                
        return render(request, template_name=self.template_name, context=self.context)