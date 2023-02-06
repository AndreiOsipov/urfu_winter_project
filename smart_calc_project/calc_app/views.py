from .models import Equipment, EquipmentType
from django import forms
from .forms import FlatForm, CountryHouseForm, HouseForm, OutputForm, ExcelForm
from .parser import ExcelParser, ExcelEquipment

from django.shortcuts import render
from django.views import View

class CalculatorView(View):
    template_name = 'calc_app/calc_page.html'
    people_num = 1
    flat_form = FlatForm()
    country_house_form = CountryHouseForm()
    house_form = HouseForm()
    excel_form = ExcelForm()

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
        'excel_form': excel_form
    }
    def __create_or_get_equipment_type(self, equipment_type_name: str) -> EquipmentType:
        type_queryset = EquipmentType.objects.filter(type_name = equipment_type_name)
        if type_queryset.count() == 0:
            equipment_type = EquipmentType.objects.create(type_name=equipment_type_name, type_discount=0)
            equipment_type.save()
        else:
            equipment_type = type_queryset.first()
        return equipment_type
        
    def __create_or_update_equipment_with_type(self, equipment: ExcelEquipment):
        equipment_type = self.__create_or_get_equipment_type(equipment.equipment_type)
        equipments_set = Equipment.objects.filter(equipment_id = equipment.id)
        try:
            if equipments_set.count() == 0:
                Equipment.objects.create(
                    equipment_name = equipment.name,
                    equipment_price = equipment.price,
                    equipment_id = equipment.id,
                    equipment_type = equipment_type
                ).save()
            else:
                equipments_set.update(
                    equipment_name = equipment.name,
                    equipment_price = equipment.price)
        except:
            pass

    def __get_sumbitted_form(self, name_form, post_data, file_data=None):
        if name_form == 'flat_form':
            return FlatForm(post_data)
        if name_form == 'country_house_form':
            return CountryHouseForm(post_data)
        if name_form == 'house_form':
            return HouseForm(post_data)
        if name_form == 'excel_form':
            return ExcelForm(post_data, file_data)

    def get(self, request):
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request):

        name_form = request.POST.get('action')
        submitted_form = self.__get_sumbitted_form(name_form,request.POST, request.FILES)
        if submitted_form.is_valid():
            self.context[name_form]=submitted_form
            
            form_data = submitted_form.cleaned_data
            if name_form == 'excel_form':#разобраться, какие атрибуты имеет fileFiled
                uploaded_file = form_data['input_excel']
                parser = ExcelParser()
                lst = parser.generate_equipment_list(uploaded_file)
                

                for excel_equipment in lst:
                    self.__create_or_update_equipment_with_type(excel_equipment)
            
        return render(request, template_name=self.template_name, context=self.context)