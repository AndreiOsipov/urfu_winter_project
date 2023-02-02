from django.db import models
from django.db.models.functions import Length

models.CharField.register_lookup(Length)

class EquipmentType(models.Model):
    type_name = models.CharField(max_length=50, primary_key=True)
    type_discount = models.FloatField()
    
    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f'{self.type_name.__str__()}'

class Equipment(models.Model):
    equipment_name = models.CharField(max_length=40) 
    equipment_price = models.FloatField()
    equipment_id = models.CharField(max_length=7)
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(name='equipment_id_like', check=models.Q(equipment_id__length__gte=7)),
            models.CheckConstraint(name='price_gte_zero', check=models.Q(equipment_price__gte=0)),            
        ]
        verbose_name = 'Оборудование'
        verbose_name_plural = verbose_name


class AbsrtactAnalysisDataModel(models.Model):

    field_str_dict = {}
    def get_str_value_with_choice(self, field):
        pass
    def get_str_value_no_choice(self, field):
        pass
    
    def add_field(self, field_name: str, field, label:str):
        
        if hasattr(field, 'choice'):
            self.field_str_dict[field] = (label, self.get_str_value_with_choice)
        else:
            self.field_str_dict[field] = (label, self.get_str_value_no_choice)
        
        super().add_to_class(self, field_name, field)

    def __str__(self) -> str:        
        print(self.field_str_dict)
        result = ''
        
        return super().__str__()

    class Meta:
        verbose_name = ''
        abstract = True
        verbose_name_plural = verbose_name

class FlatHouseWithWaterAnalysis(AbsrtactAnalysisDataModel):
    choices_for_hardness = [(0, 'до 3'), (3, 'до 7'), (7, 'от 7')]
    choices_for_ferum = [(0, 'до 0,6'),(0.6, 'до 0,9'), (0.9, 'от 0,9')]

    class Meta(AbsrtactAnalysisDataModel.Meta):
        verbose_name = 'данные о воде в квартире, когда есть анализ'

class CountryHouseWithWaterAnalysis(AbsrtactAnalysisDataModel):
    choices_for_ferum = [(0, 'до 0,3'), (0.3, 'до 0,9'), (0.9, 'от 0,9')]
    choices_for_vater_v = [(1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)')]
    
    water_v_used_per_hour = models.FloatField(choices=choices_for_vater_v)
    water_smell = models.BooleanField()

    class Meta(AbsrtactAnalysisDataModel.Meta):
        verbose_name = 'данные для деревенского дома с анализом воды'

class BaseHouseWithWaterAnalysis(AbsrtactAnalysisDataModel):
    
    #отнаследовать модели
    #water_v_used_per_hour = models.FloatField(choices=[(1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)'), (2.0, '5 - 8 человек (до 2,5-х куб.м./ч)'), (2.5, '8 и более человек(от 2,5 - х куб.м./ч)')])
    #water_hardness = models.IntegerField(choices=[(0, 'до 3'),(3, 'до 8'),(8, 'до 15'), (20, 'от 15')])
    #water_ferum = models.FloatField(choices=[(0, 'до 0,3'), (0.3, 'до 0,9'), (0.9, 'до 8'), (8, 'от 8')])
    #water_mpc = models.BooleanField()
    #water_smell = models.BooleanField()

    AbsrtactAnalysisDataModel.add_field(field_name='water_v_used_per_hour', field=models.FloatField(choices=[(1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)'), (2.0, '5 - 8 человек (до 2,5-х куб.м./ч)'), (2.5, '8 и более человек(от 2,5 - х куб.м./ч)')]), label='вода в час')
    AbsrtactAnalysisDataModel.add_field('water_hardness', models.IntegerField(choices=[(0, 'до 3'),(3, 'до 8'),(8, 'до 15'), (20, 'от 15')]), 'жесткость')
    AbsrtactAnalysisDataModel.add_field('water_ferum', models.FloatField(choices=[(0, 'до 0,3'), (0.3, 'до 0,9'), (0.9, 'до 8'), (8, 'от 8')]), 'железо')
    AbsrtactAnalysisDataModel.add_field('water_mpc', models.BooleanField(), 'другое')
    AbsrtactAnalysisDataModel.add_field('water_smell', models.BooleanField(),'запах')
    class Meta:
        verbose_name = 'данные для коттеджа, когда есть анализ воды'
        unique_together = ['water_v_used_per_hour','water_hardness','water_ferum','water_mpc','water_smell']
        verbose_name_plural = verbose_name


class BaseHouseAnalysisEquimpent(models.Model):
    input_data = models.ForeignKey(BaseHouseWithWaterAnalysis, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['input_data','equipment']
        verbose_name = 'оборудование, подходящее для установки в коттедж, когда есть анализ воды'
        verbose_name_plural = verbose_name

class BaseHouseWithoutWaterAnalysis(models.Model):
    water_v_used_per_hour = models.FloatField(choices=[(1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)'), (2.0, '5 - 8 человек (до 2,5-х куб.м./ч)'), (2.5, '8 и более человек(от 2,5 - х куб.м./ч)')])
    water_hardness = models.BooleanField()
    water_ferum = models.BooleanField()
    water_smell = models.BooleanField()

    class Meta:
        unique_together = ['water_v_used_per_hour', 'water_hardness', 'water_ferum', 'water_smell']
        verbose_name = 'данные для коттеджа, когда нет анализа воды'
        verbose_name_plural = verbose_name

class BaseHouseNoAnalysisEquipment(models.Model):
    input_data = models.ForeignKey(BaseHouseWithoutWaterAnalysis, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['input_data','equipment']
        verbose_name = 'оборудование, подходящее для установки в коттедж, когда нет анализа воды'
        verbose_name_plural = verbose_name

class CoutryHouseAnalysisEquipment(models.Model):
    input_data = models.ForeignKey(CountryHouseWithWaterAnalysis, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['input_data','equipment']
        verbose_name = 'оборудование, подходящее для установки на дачу, когда есть анализ воды'
        verbose_name_plural = verbose_name

class CountryHouseWithoutWaterAnalysis(models.Model):
    water_v_used_per_hour = models.FloatField(choices=[(1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)')])
    water_hardness = models.BooleanField()
    water_ferum = models.BooleanField()
    water_smell = models.BooleanField()

    class Meta:
        unique_together = ['water_v_used_per_hour', 'water_hardness', 'water_ferum', 'water_smell']
        verbose_name = 'данные о воде для дачи, когда нет анализа воды'
        verbose_name_plural = verbose_name
        
class CountryHouseNoAnalysisEquipment(models.Model):
    input_data = models.ForeignKey(CountryHouseWithoutWaterAnalysis, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['input_data','equipment']
        verbose_name = 'оборудование для установки на дачу, когда нет анализа воды'
        verbose_name_plural = verbose_name


class FlatHouseAnalysisEquipment(models.Model):
    input_data = models.ForeignKey(FlatHouseWithWaterAnalysis, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['input_data','equipment']
        verbose_name = 'квартирные фильтры, когда есть анализ воды'
        verbose_name_plural = verbose_name

class FlatHouseWithoutWaterAnalysis(models.Model):
    water_harness = models.BooleanField()
    water_ferum = models.BooleanField()

    class Meta:
        unique_together = ['water_harness','water_ferum']
        verbose_name = 'данные о воде для квартиры без анализа'
        verbose_name_plural = verbose_name

class FlatHouseNoAnalysisEquipment(models.Model):
    inout_data = models.ForeignKey(FlatHouseWithoutWaterAnalysis, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['inout_data','equipment']
        verbose_name = 'фильтры для квартир, когда нет анализа воды'
        verbose_name_plural = verbose_name
class AbsrtactNoAnalysisDataModel(models.Model):
    water_hardness = models.BooleanField()
    water_ferum = models.BooleanField()
    
    class Meta:
        abstract = True