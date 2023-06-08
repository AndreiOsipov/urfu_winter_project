import os
from django.core.exceptions import ValidationError
from django import forms
from django.db.models import QuerySet
from .genereator_for_fields import ChoicesGenerator
from .models import (
    Complects, 
    Equipments,  
    Fillers,
    FullWaterParametrs,
    WaterConsumptionLevel,
    MontageWork)

class FloatChoiceField(forms.ChoiceField):
    def to_python(self, value):
        return float(super().to_python(value))

class NamePriceRow:
    '''
    нужен, имя и цену оборудования сгруппировать в одну строку
    '''
    def __init__(self, name_form, price_form, row_id) -> None:
        self.name_form = name_form
        self.price_form = price_form
        self.row_id = row_id

    def __str__(self) -> str:
        return f'{self.name_form} --- {self.price_form} --- {self.row_id}'
class EditComplectForm(forms.Form):
    form_name = forms.CharField(max_length=20, initial='confirm_form', widget=forms.HiddenInput,required=False)
    client_first_name = forms.CharField(max_length=50, label='имя клиента',required=False)
    client_last_name = forms.CharField(max_length=50, label='фамилия клиента',required=False)
    client_phone_number = forms.CharField(max_length=10, label='номер телефона клиента',required=False)

    builder_type = forms.CharField(max_length=50,label='тип объекта',required=False)
    montage_place = forms.CharField(max_length=50, label='место установки',required=False)
    main_water_source = forms.CharField(max_length=50, label='основной источник воды',required=False)
    sewerage_type = forms.CharField(max_length=50, label='тип канализации',required=False)
    

    def __generate_equipments_field(self, equipment: Equipments):
        equipments_with_same_type = Equipments.objects.filter(equipment_type = equipment.equipment_type)
        return forms.ChoiceField(
            choices=list(map(lambda found_equipment: (found_equipment.name,found_equipment.name), equipments_with_same_type)),
            initial=(equipment.name, equipment.name), label='')
    
    def __generate_equipment_price_field(self, equipment: Equipments):
        return forms.FloatField(initial=equipment.price)
    
    def __get_equipment_type_equipment_dict(self):
        equipment_type_equipment_dict:dict[str, list[Equipments]] = {}
        all_equipments = Equipments.objects.all()
        for equipment in all_equipments:
            type_name = equipment.equipment_type.name
            if type_name in equipment_type_equipment_dict.keys():
                equipment_type_equipment_dict[type_name].append(equipment)
        return equipment_type_equipment_dict
    
    def __get_fillers_choices(self):
        all_fillers = Fillers.objects.all()
        return [
            (filler.id, filler.name)
            for filler in all_fillers
        ]
    
    def __init__(self,complect:Complects=None,filler:Fillers=None,water_consumption_level:WaterConsumptionLevel=None,water_paramers:FullWaterParametrs=None, not_edited_data = None) -> None:
        super(EditComplectForm, self).__init__(data=not_edited_data)       

        if not (complect is None):
            equipments_for_complect = Equipments.objects.filter(complects = complect)
            equipment_type_equipment_dict = self.__get_equipment_type_equipment_dict()
            
            fillers = Fillers.objects.all()
            # complect_fillers = fillers.filter(complect = complect)

            ind = 0
            self.equipments_fields = []
            self.montage_works_fields = []
            self.complect = complect
            
            self.fields[f'complect'] = forms.ChoiceField(choices=[(complect.id,complect.name)], label='комлект')
            montage_works = MontageWork.objects.filter(complects = complect)

            for equipment in equipments_for_complect:
                equipmnt_field = self.__generate_equipments_field(equipment)
                equipment_price_field = self.__generate_equipment_price_field(equipment)

                self.fields[f'equipment_name_{ind}'] = equipmnt_field
                self.fields[f'equipment_price_{ind}'] = equipment_price_field
                self.fields[f'equipment_id_{ind}'] = forms.CharField(max_length = 20, initial=equipment.id, widget=forms.HiddenInput())
                # self.fields[f'docs'] = forms.FileField(initial=word_docx)
                self.equipments_fields.append(NamePriceRow(self[f'equipment_name_{ind}'], self[f'equipment_price_{ind}'], self[f'equipment_id_{ind}']))
                ind += 1
            
            ind = 0
            for montage_work in montage_works:
                self.fields[f'montage_work_name_{ind}'] = forms.CharField(max_length=50,initial=montage_work.name)
                self.fields[f'montage_work_price_{ind}'] = forms.FloatField(initial=montage_work.price)
                self.fields[f'montage_work_id_{ind}'] = forms.CharField(max_length=20,initial=montage_work.id, widget=forms.HiddenInput())
                self.montage_works_fields.append(NamePriceRow(self[f'montage_work_name_{ind}'], self[f'montage_work_price_{ind}'],self[f'montage_work_id_{ind}']))
                ind+=1

            fillers_choices = self.__get_fillers_choices()
            self.fields['filler'] = forms.ChoiceField(choices=fillers_choices,initial=(filler.id, filler.name),required=False)
            self.fields['filler_price'] = forms.FloatField(initial=filler.price)
            
            self.fields['water_consumption_level_id'] = forms.CharField(max_length=20,initial=water_consumption_level.id, widget=forms.HiddenInput())
            self.fields['full_water_parametrs_id'] = forms.CharField(max_length=20, initial=water_paramers.id, widget=forms.HiddenInput())

class ComplectSearchForm(forms.Form):
    choices_generator = ChoicesGenerator()

    form_name = forms.CharField(max_length=50, initial='search_form')
    water_consumption = FloatChoiceField(
        choices=[
            (1.2,'до 1,2 М3/Ч 3 точки (пример: 2 крана и душ)'),
            (1.8,'до 1,8 М3/Ч 4-5 точек (пример: 2 крана, стиральная машина/посудомоечная машина, душ) (пиктограммами)'),
            (2.4,'до 2,4 М3/Ч 4-5 точек большего объема (пример: 2 крана, стиральная машина и посудомоечная машина, тропический душ)'),
            (3,'до 3 М3/Ч от 5 точки большего объема (пример: бассейн, или 2 крана, стиральная машина и посудомоечная машина, тропический душ)')
            ],
        label='расход воды')
    
    people_number = FloatChoiceField(choices=[(3,'до 3'), (4, 'до 4'), (5, 'до 5'), (6,'до 6'), (7,'до 7')], label='количество человек')
    condensation_protection = forms.BooleanField(required=False, label='нужна защита от конденсата')

    hardness = FloatChoiceField(choices=choices_generator.generate_choices(0,16,1), label='жесткость')
    ferum = FloatChoiceField(choices=choices_generator.generate_choices(0,16,1), label='железо')
    po = FloatChoiceField(choices=choices_generator.generate_choices(0,16,1), label='по')
    hydrogen_sulfite = FloatChoiceField(choices=choices_generator.generate_choices(0,6,1), label='сероводород')
    ammonium = FloatChoiceField(choices=choices_generator.generate_choices(0,6,1), label='аммоний')
    manganese = FloatChoiceField(choices=choices_generator.generate_choices(0,6,1), label='марганец')


def init_from_digits(
    water_consumption=None,
    people_number=None,
    hardness=None,
    ferum=None,
    po=None,
    hydrogen_sulfite=None,
    ammonium=None,
    manganese=None,
    condensation_protection=False
    ):

    water_consumptions_tuple_matches = {
        1.2:(1.2,'до 1,2 М3/Ч 3 точки (пример: 2 крана и душ)'),
        1.8:(1.8,'до 1,8 М3/Ч 4-5 точек (пример: 2 крана, стиральная машина/посудомоечная машина, душ) (пиктограммами)'),
        2.4:(2.4,'до 2,4 М3/Ч 4-5 точек большего объема (пример: 2 крана, стиральная машина и посудомоечная машина, тропический душ)'),
        3.0:(3,'до 3 М3/Ч от 5 точки большего объема (пример: бассейн, или 2 крана, стиральная машина и посудомоечная машина, тропический душ)')
    }

    people_number_tuple_matches = {
    3: (3,'до 3'),
    4: (4,'до 4'),
    5: (5,'до 5'),
    6: (6,'до 6'),
    7: (7,'до 7'),
    }
    print(f'кортеж, обозначающий количество людей: {people_number_tuple_matches}')
    choices_generator = ChoicesGenerator()
    hardness_tuple = choices_generator.generate_tuple(hardness)
    ferum_tuple = choices_generator.generate_tuple(ferum)
    po_tuple = choices_generator.generate_tuple(po)
    hydrogen_sulfite_tuple = choices_generator.generate_tuple(hydrogen_sulfite)
    ammonium_tuple = choices_generator.generate_tuple(ammonium)
    manganese_tuple = choices_generator.generate_tuple(manganese)
    condensation_protection_tuple = choices_generator.generate_tuple(condensation_protection)
    print(
        f'ferum: {ferum_tuple},\n \
        hardness: {hardness_tuple},\n \
        hydrogen: {hydrogen_sulfite_tuple},\n \
        ammonium: {ammonium_tuple},')
    
    return ComplectSearchForm(
        data={
            "form_name":"search_form",
            "water_consumption":water_consumptions_tuple_matches[water_consumption],
            "people_number_tuple_matches":people_number_tuple_matches[people_number],
            "hardness":hardness_tuple,
            "ferum":ferum_tuple,
            "po":po_tuple,
            "hydrogen_sulfite":hydrogen_sulfite_tuple,
            "ammonium":ammonium_tuple,
            "manganese":manganese_tuple,
        })