from .models import Equipment, EquipmentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, HttpResponse
import io 
import os
from .forms import (NumberFlatForm, 
    NumberCountryHouseForm, 
    NumberHouseForm,
    BoolFlatForm,
    BoolCountryHouseForm,
    BoolBaseHouseForm,
    ExcelForm,
    OutputForm)

from .order_file_handler.parser import ExcelParser
from .order_file_handler.marker import ExcelMarker

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
    
    context = {
        'flat_form': flat_form,
        'country_form': country_house_form,
        'house_form': house_form,
        'bool_flat_form': bool_flat_form,
        'bool_country_form':bool_country_house_form,
        'bool_house_form':bool_house_form,
        'excel_form': excel_form,
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
                parsed_excel = parser.get_parsed_excel(uploaded_file)
                readed_file=  ExcelMarker().get_marked_pricelist(uploaded_file, parsed_excel.not_full_rows_indexes, color='00FFFF00')
                
                for excel_equipment in parsed_excel.equipment_list:
                    equipment_type, was_created = EquipmentType.objects.get_or_create(type_name = excel_equipment.type, type_discount = 0)
                    Equipment.objects.update_or_create(
                        equipment_name = excel_equipment.name,
                        equipment_price = excel_equipment.price,
                        equipment_id = excel_equipment.id,
                        equipment_type = equipment_type)
                return HttpResponse(content=readed_file, headers={
                    'Content-Type': 'calc_app/vnd.ms-excel',
                    'Content-Disposition': 'attachemnt; filename="pricelist.xlsx"'
                })
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