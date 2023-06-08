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
    WaterConsumptionLevel, MontageWork, Client)

from .forms import ComplectSearchForm, EditComplectForm, NamePriceRow, init_from_digits
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
        # print(requst.GET)
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
    def __fill_row_dict(self,raw_dict, row_dict, row_part_key):
        for key in raw_dict:
            if row_part_key in key:
                if key[-1] not in row_dict.keys():
                    row_dict[key[-1]] = NamePriceRow(None,None,None)
                if 'name' in key:
                    row_dict[key[-1]].name_form = raw_dict[key]
                if 'price' in key:
                    row_dict[key[-1]].price_form = raw_dict[key]
                if '_id_' in key:
                    row_dict[key[-1]].row_id = raw_dict[key]
    
    def _get_data_from_raw_queryset(self, raw_querydict):
        complect_id = raw_querydict['complect']
        filler_id = raw_querydict['filler']
        
        self.complect = Complects.objects.filter(id=complect_id).first()
        self.column = self.complect.column

        self.filler = Fillers.objects.filter(id=filler_id).first()
        self.filler_price = round(float(raw_querydict['filler_price']),2)
        
        water_consumption_id = raw_querydict['water_consumption_level_id']
        full_water_parametrs_id = raw_querydict['full_water_parametrs_id']
        
        self.water_consumption = WaterConsumptionLevel.objects.filter(id=water_consumption_id).first()
        self.water_parametrs = FullWaterParametrs.objects.filter(id=full_water_parametrs_id)

        client_first_name = raw_querydict['client_first_name']
        client_last_name = raw_querydict['client_last_name']
        client_phone_number = raw_querydict['client_phone_number']
        self.client = Client.objects.create(first_name = client_first_name, last_name = client_last_name, phone_number = client_phone_number)
        self.client.save()

        builder_type = raw_querydict['builder_type']
        montage_place = raw_querydict['montage_place']
        main_water_source = raw_querydict['main_water_source']
        sewerage_type = raw_querydict['sewerage_type']
        self.builder_object = BuilderObject.objects.create(builder_type=builder_type,main_water_source=main_water_source, montage_place=montage_place,sewerage_type=sewerage_type)
        
        self.builder_object.save()
        raw_dict = raw_querydict.dict()
        
        self.row_equipments_dict = {}# словарь, в котором номер строки сопоставляется с классом строки
        self.row_montage_dict = {}

        self.__fill_row_dict(raw_dict,self.row_equipments_dict,'equipment_')
        self.__fill_row_dict(raw_dict,self.row_montage_dict,'montage_work_')
        
        
    
    def post(self, request):
        generator = DocxGenerator()
        not_cleaned_data = request.POST
        print(request.POST)
        edit_complect_form = EditComplectForm(not_edited_data=not_cleaned_data)
        if edit_complect_form.is_valid():
            

            data = edit_complect_form.cleaned_data
            self._get_data_from_raw_queryset(not_cleaned_data)

            word_docx = generator.generate_contract(self.complect,self.water_parametrs,self.client,self.builder_object,self.water_consumption)
            contract_file = word_docx
            return FileResponse(contract_file, filename='contact.docx')
        print(edit_complect_form.errors)
        return render(request, template_name='calc_app/empty_page.html')