from django.db import models
from django.db.models.functions import Length

models.CharField.register_lookup(Length)

class EquipmentType(models.Model):
    type_name = models.CharField(max_length=50, primary_key=True)
    type_discount = models.FloatField()

class Equipment(models.Model):
    equipment_name = models.CharField(max_length=40, verbose_name='название')
    equipment_price = models.FloatField(verbose_name='цена')
    equipment_id = models.CharField(max_length=7)
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE,verbose_name='Тип оборудования')

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = verbose_name
        constraints = [
            models.CheckConstraint(name='equipment_id_like', check=models.Q(equipment_id__length__gte=7)),
            models.CheckConstraint(name='price_gte_zero', check=models.Q(equipment_price__gte=0)),            
        ]

class BaseHouseWithWaterAnalysis(models.Model):
    water_v_used_per_hour = models.FloatField(choices=[(1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)'), (2.0, '5 - 8 человек (до 2,5-х куб.м./ч)'), (2.5, '8 и более человек(от 2,5 - х куб.м./ч)')])
    water_hardness = models.IntegerField(choices=[(0, 'до 3'),(3, 'до 8'),(8, 'до 15'), (20, 'от 15')])
    water_ferum = models.FloatField(choices=[(0, 'до 0,3'), (0.3, 'до 0,9'), (0.9, 'до 8'), (8, 'от 8')])
    water_mpc = models.BooleanField()
    water_smell = models.BooleanField()

    class Meta:
        unique_together = ['water_v_used_per_hour','water_hardness','water_ferum','water_mpc','water_smell']
        verbose_name_plural = verbose_name


class FlatHouseWithoutWaterAnalysis(AbstractHouse):
    fiedls_names_for_str = [
        'water_hardness',
        'water_ferum']
    water_hardness = models.BooleanField(verbose_name='жесткость',default=False)
    water_ferum = models.BooleanField(verbose_name='железо')

    class Meta:
        verbose_name = 'Квартира, нет анализа'
        verbose_name_plural = verbose_name
        unique_together = ['water_hardness','water_ferum']

class CountryHouseWithoutWaterAnalysis(AbstractHouse):
    water_v_used_per_hour = models.FloatField(choices=[
            (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'),
            (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)')],
            verbose_name='лидей в доме')
    water_hardness = models.BooleanField(verbose_name='жесткость')
    water_ferum = models.BooleanField(verbose_name='железо')
    water_smell = models.BooleanField(verbose_name='запах')
    fiedls_names_for_str = [
        'water_v_used_per_hour',
        'water_hardness',
        'water_ferum',
        'water_smell',
    ]
    class Meta:
        verbose_name = 'Дача, нет анализа'
        verbose_name_plural = verbose_name
        unique_together = ['water_v_used_per_hour', 'water_hardness', 'water_ferum', 'water_smell']

class BaseHouseWithoutWaterAnalysis(AbstractHouse):
    water_v_used_per_hour = models.FloatField(choices=[
        (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), 
        (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)'), 
        (2.0, '5 - 8 человек (до 2,5-х куб.м./ч)'), 
        (2.5, '8 и более человек(от 2,5 - х куб.м./ч)')],
        verbose_name='людей в доме')
    water_hardness = models.BooleanField(verbose_name='жесткость')
    water_ferum = models.BooleanField(verbose_name='железо')
    water_smell = models.BooleanField(verbose_name='запах')

    fiedls_names_for_str = [
        'water_v_used_per_hour',
        'water_hardness',
        'water_ferum',
        'water_smell',
    ]

    class Meta:
        verbose_name = 'Коттедж, нет анализа'
        verbose_name_plural = verbose_name
        unique_together = ['water_v_used_per_hour', 'water_hardness', 'water_ferum', 'water_smell']

class BaseHouseAnalysisEquimpent(models.Model):
    input_data = models.ForeignKey(BaseHouseWithWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')
    
    class Meta:
        verbose_name = 'Коттедж --  борудование (есть анализ)'
        verbose_name_plural = verbose_name
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

class BaseHouseNoAnalysisEquipment(models.Model):
    input_data = models.ForeignKey(BaseHouseWithoutWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

    class Meta:
        verbose_name = 'Коттедж --  борудование (нет анализа)'
        verbose_name_plural = verbose_name
        unique_together = ['input_data','equipment']

class CountryHouseWithWaterAnalysis(models.Model):
    water_v_used_per_hour = models.FloatField(choices=[(1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)')])
    water_hardness = models.IntegerField(choices=[(0, 'до 3'), (3, 'до 7'), (7, 'от 7')])
    water_ferum = models.FloatField(choices=[(0, 'до 0,3'),(0.3, 'до 0,9'),(0.9, 'от 0,9')])
    water_mpc = models.BooleanField()
    water_smell = models.BooleanField()

    class Meta:
        unique_together = ['water_v_used_per_hour','water_hardness','water_ferum','water_mpc','water_smell']

class CoutryHouseAnalysisEquipment(models.Model):
    
    input_data = models.ForeignKey(CountryHouseWithWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

    class Meta:
        verbose_name = 'Дача --  борудование (есть анализ)'
        verbose_name_plural = verbose_name
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

class CountryHouseNoAnalysisEquipment(models.Model):
    input_data = models.ForeignKey(CountryHouseWithoutWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

    class Meta:
        verbose_name = 'Дача --  борудование (нет анализа)'
        verbose_name_plural = verbose_name
        unique_together = ['input_data','equipment']

class FlatHouseWithWaterAnalysis(models.Model):
    water_hardness = models.IntegerField(choices=[(0, 'до 3'), (3, 'до 7'), (7, 'от 7')])
    water_ferum = models.FloatField(choices=[(0, 'до 0,6'),(0.6, 'до 0,9'), (0.9, 'от 0,9')])
    water_mpc = models.BooleanField()
    
    class Meta:
        unique_together = ['water_hardness','water_ferum','water_mpc']

class FlatHouseAnalysisEquipment(models.Model):
    
    input_data = models.ForeignKey(FlatHouseWithWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

    class Meta:
        verbose_name = 'Квартира --  борудование (есть анализ)'
        verbose_name_plural = verbose_name
        unique_together = ['input_data','equipment']
        verbose_name = 'квартирные фильтры, когда есть анализ воды'
        verbose_name_plural = verbose_name

class FlatHouseWithoutWaterAnalysis(models.Model):
    water_harness = models.BooleanField()
    water_ferum = models.BooleanField()

    class Meta:
        unique_together = ['water_harness','water_ferum']

class FlatHouseNoAnalysisEquipment(models.Model):
    inout_data = models.ForeignKey(FlatHouseWithoutWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

    class Meta:
        verbose_name = 'Капртира --  борудование (нет анализа)'
        verbose_name_plural = verbose_name
        unique_together = ['inout_data','equipment']
        verbose_name = 'фильтры для квартир, когда нет анализа воды'
        verbose_name_plural = verbose_name
class AbsrtactNoAnalysisDataModel(models.Model):
    water_hardness = models.BooleanField()
    water_ferum = models.BooleanField()
    
    class Meta:
        abstract = True