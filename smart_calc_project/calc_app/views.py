from django.views import View
from django.shortcuts import render
from .models import (
    BuilderObject,
    FullWaterParametrs,
    Columns,
    Complects,
    Equipments,
    ComplectsEquipments,
    Fillers, 
    WaterConsumptionLevel, MontageWork)

from .forms import ComplectSearchForm, EditComplectForm, init_from_digits
from .word_generator import DocxGenerator
from django.http import FileResponse

class GetSearcheForm(View):

    template_name = 'calc_app/calc_page.html'

    def get(self, request):
        form = ComplectSearchForm()    
        return render(request, self.template_name, context = {'search_form': form})

class GetComplectView(View):
    template_name = 'calc_app/calc_page.html'
    
    def get(self, requst):
        # собрать заново форму
        # проверить на валидность
        # вернуть шаблон с формой и, если она валидна вторую форму с найденным комплектом 
        form_parametrs = requst.GET
        water_consumption = float(form_parametrs['water_consumption'])
        people_number = int(form_parametrs['people_number'])
        hardness = float(form_parametrs['hardness'])
        ferum = float(form_parametrs['ferum'])
        po = int(form_parametrs['po'])
        hydrogen_sulfite = float(form_parametrs['hydrogen_sulfite'])
        ammonium = float(form_parametrs['ammonium'])
        manganese = float(form_parametrs['manganese'])
        
        if 'condensation_protection' in form_parametrs:
            condensation_protection = True
            print('нужна защита от конденсата')
        
        form = init_from_digits(
            water_consumption,
            people_number,
            hardness,
            ferum,
            po,
            hydrogen_sulfite,
            ammonium,
            manganese,
            )
        print(requst.GET)
        water_parametrs = FullWaterParametrs.objects.filter(
            hardness=hardness,
            ferum = ferum,
            po = po,
            hydrogen_sulfite = hydrogen_sulfite,
            ammonium = ammonium,
            manganese = manganese
        ).first()

        if not(water_parametrs is None):
            water_consumption_level = WaterConsumptionLevel.objects.filter(water_consumption=water_consumption,people_number = people_number).first()
            complect = Complects.objects.filter(full_water_parametrs = water_parametrs, water_consumption_level=water_consumption_level).first()
            filler = Fillers.objects.filter(full_water_parametrs = water_parametrs, water_consumption_level=water_consumption_level).first()
        
            if not(complect is None or filler is None):
                montage_works = MontageWork.objects.filter(complects = complect)
                edit_complect_form = EditComplectForm(complect, filler, water_consumption_level, water_parametrs)
                return render(requst,template_name=self.template_name,context={'search_form': form, 'edit_form': edit_complect_form})
        return render(requst,template_name=self.template_name,context={'search_form': form})
    
class GetContractView(View):
    
    def get(self, request):
        generator = DocxGenerator()
        data = request.GET
        print(data)

        complect_id = data['complect_id']
        builder_object_id = data['builder_object_id']
        full_water_parametrs_id = data['full_water_parametrs_id']
        filler_id = data['filler_id']
        

        complect = Complects.objects.get(id = complect_id)
        builder_object = BuilderObject.objects.get(id = builder_object_id)

        word_docx = generator.generate_contract(complect, builder_object)
        contract_file = word_docx
        return FileResponse(contract_file, filename='contact.docx')