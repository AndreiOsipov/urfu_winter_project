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
        condensation_protection = False
        
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
            condensation_protection
            )
        
        water_parametrs = FullWaterParametrs.objects.filter(
            hardness=hardness,
            ferum = ferum,
            po = po,
            hydrogen_sulfite = hydrogen_sulfite,
            ammonium = ammonium,
            manganese = manganese
        ).first()
        water_consumption_level = WaterConsumptionLevel.objects.filter(water_consumption=water_consumption,people_number = people_number).first()
        complect = Complects.objects.filter(full_water_parametrs = water_parametrs, water_consumption_level=water_consumption_level).first()
        filler = Fillers.objects.filter(full_water_parametrs = water_parametrs, water_consumption_level=water_consumption_level).first()
        
        if not(complect is None):
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































































# class SearcherVew(View):

#     def get(self, request):
#         # <view logic>
#         print(f'-->> session is {request.session}')
#         calc_form = ComplectSearchForm()

#         return render(request, template_name='calc_app/calc_page.html', context={'complect_search_form':calc_form})
    
#     def post(self, request):
#         form_name = request.POST.get('form_name')
#         print(form_name)

#         if form_name == 'search_form':
#             submitted_form = ComplectSearchForm(request.POST)
#         if form_name == 'confirm_form':
#             # print(request.POST.get('complect'))
#             submitted_form = ComplectConfirmationForm(None,None,None,None,request.POST)

#         print(request.POST)
#         if submitted_form.is_valid():
            
#             # print(word_docx)
#             if form_name == 'search_form':
#                 data = submitted_form.cleaned_data
#                 full_water_parametrs = FullWaterParametrs.objects.filter(
#                 hardness=data['hardness'],
#                 ferum=data['ferum'],
#                 po=data['po'],
#                 hydrogen_sulfite=data['hydrogen_sulfite'],
#                 ammonium=data['ammonium'],
#                 manganese=data['manganese']).first()
#                 object_info = BuilderObject.objects.filter(water_consumption=data['water_consumption']).first()
#                 print('type object info: ',type(object_info))
#                 print(full_water_parametrs)
#                 complect = Complects.objects.filter(builder_object=object_info).filter(full_water_parametrs=full_water_parametrs).first()
#                 filler = Fillers.objects.filter(builder_object=object_info, full_water_parametrs=full_water_parametrs).first()
#                 print(complect, type(complect))
#                 generator = DocxGenerator()
#                 word_docx = generator.generate_deal(complect, object_info, full_water_parametrs)
#                 files['a'] = word_docx
#                 confirm_form = ComplectConfirmationForm(complect,full_water_parametrs,object_info,filler,word_docx)

#                 return render(request, template_name='calc_app/calc_page.html', context={
#                     'complect_search_form':submitted_form, 
#                     'confirm_form': confirm_form})
#         else:
#             return FileResponse(files['a'], filename='doc.docx')
        
# class SignAgreementView(View):
#     def get(self):
#         return render()