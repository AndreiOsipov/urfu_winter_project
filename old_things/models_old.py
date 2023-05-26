from django.db import models
from django.db.models.functions import Length

models.CharField.register_lookup(Length)

class EquipmentType(models.Model):
    type_name = models.CharField(max_length=50, primary_key=True, verbose_name='тип оборудования')
    type_discount = models.FloatField(verbose_name='скидка')

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'

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
    def __str__(self) -> str:
        return self.equipment_name
        
class AbstractHouse(models.Model):   
    fiedls_names_for_str = []

    def get_str_field(self, field):
        str_field = ''
        if field.verbose_name:
            str_field += f'{field.verbose_name} '
        if field.choices:
            for choice in field.choices:
                if choice[0] == field.value_from_object(self):
                    str_field+=f'{choice[1]} '
        else:
            if field.value_from_object(self):
                str_field+='Да '
            else:
                str_field += 'Нет '
        return str_field

    def __str__(self) -> str:
        #прикрепить ->:<-
        #
        #
        str_r = ''
        for field_name in self.fiedls_names_for_str:
            field = self._meta.get_field(field_name)
            str_r += self.get_str_field(field)
        return str_r

    class Meta:
        abstract = True

class FlatHouseWithWaterAnalysis(AbstractHouse):
    fiedls_names_for_str = [
        'water_hardness',
        'water_ferum',
        'water_mpc',
    ]

    water_hardness = models.IntegerField(choices=[(0, 'до 3'), (3, 'до 7'), (7, 'от 7')], verbose_name='жесткость')
    water_ferum = models.FloatField(choices=[(0, 'до 0,6'),(0.6, 'до 0,9'), (0.9, 'от 0,9')], verbose_name='железо')
    water_mpc = models.BooleanField(verbose_name='Другие примеси')
    equipments = models.ManyToManyField(Equipment, through='FlatHouseAnalysisEquipment')

    class Meta:
        verbose_name = 'Квартира, есть анализ'
        verbose_name_plural = verbose_name
        unique_together = ['water_hardness','water_ferum','water_mpc']

class CountryHouseWithWaterAnalysis(AbstractHouse):
    fiedls_names_for_str = [
        'water_v_used_per_hour',
        'water_hardness',
        'water_ferum',
        'water_mpc',
        'water_smell',
    ]
    
    water_v_used_per_hour = models.FloatField(
        choices=[
            (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), 
            (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)')],
        verbose_name='людей в доме')
    water_hardness = models.IntegerField(
        choices=[
            (0, 'до 3'),
            (3, 'до 7'),
            (7, 'от 7')],
        verbose_name='жесткость')
    water_ferum = models.FloatField(
        choices=[
            (0, 'до 0,3'),
            (0.3, 'до 0,9'),
            (0.9, 'от 0,9')],
        verbose_name='железо')
    
    water_mpc = models.BooleanField(verbose_name='другие примеси')
    water_smell = models.BooleanField('запах')
    equipments = models.ManyToManyField(Equipment, through='CoutryHouseAnalysisEquipment')

    class Meta:
        verbose_name = 'Дача, есть анализ'
        unique_together = ['water_v_used_per_hour','water_hardness','water_ferum','water_mpc','water_smell']

class BaseHouseWithWaterAnalysis(AbstractHouse):
    fiedls_names_for_str = [
        'water_v_used_per_hour',
        'water_hardness',
        'water_ferum',
        'water_mpc',
        'water_smell',
    ]

    water_v_used_per_hour = models.FloatField(choices=[
            (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'),
            (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)'),
            (2.0, '5 - 8 человек (до 2,5-х куб.м./ч)'),
            (2.5, '8 и более человек(от 2,5 - х куб.м./ч)')],
        verbose_name='людей в доме')
    water_hardness = models.IntegerField(choices=[
            (0, 'до 3'),
            (3, 'до 8'),
            (8, 'до 15'),
            (20, 'от 15')], 
        verbose_name='жесткость')
    water_ferum = models.FloatField(choices=[
            (0, 'до 0,3'),
            (0.3, 'до 0,9'),
            (0.9, 'до 8'),
            (8, 'от 8')],
        verbose_name='железо')
    water_mpc = models.BooleanField(verbose_name='другие примеси')
    water_smell = models.BooleanField('запах')
    equipments = models.ManyToManyField(Equipment, through='BaseHouseAnalysisEquimpent')
    
    class Meta:
        verbose_name = 'Коттедж, есть анализ'
        verbose_name_plural = verbose_name
        unique_together = ['water_v_used_per_hour','water_hardness','water_ferum','water_mpc','water_smell']

class FlatHouseWithoutWaterAnalysis(AbstractHouse):
    fiedls_names_for_str = [
        'water_hardness',
        'water_ferum']
    
    water_hardness = models.BooleanField(verbose_name='жесткость',default=False)
    water_ferum = models.BooleanField(verbose_name='железо')    
    equipments = models.ManyToManyField(Equipment, through='FlatHouseNoAnalysisEquipment')

    class Meta:
        verbose_name = 'Квартира, нет анализа'
        verbose_name_plural = verbose_name
        unique_together = ['water_hardness','water_ferum']

class CountryHouseWithoutWaterAnalysis(AbstractHouse):
    fiedls_names_for_str = [
        'water_v_used_per_hour',
        'water_hardness',
        'water_ferum',
        'water_smell',
    ]
    
    water_v_used_per_hour = models.FloatField(choices=[
            (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'),
            (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)')],
            verbose_name='лидей в доме')
    water_hardness = models.BooleanField(verbose_name='жесткость')
    water_ferum = models.BooleanField(verbose_name='железо')
    water_smell = models.BooleanField(verbose_name='запах')
    equipments = models.ManyToManyField(Equipment, through='CountryHouseNoAnalysisEquipment')

    class Meta:
        verbose_name = 'Дача, нет анализа'
        verbose_name_plural = verbose_name
        unique_together = ['water_v_used_per_hour', 'water_hardness', 'water_ferum', 'water_smell']

class BaseHouseWithoutWaterAnalysis(AbstractHouse):
    fiedls_names_for_str = [
        'water_v_used_per_hour',
        'water_hardness',
        'water_ferum',
        'water_smell',
    ]

    water_v_used_per_hour = models.FloatField(choices=[
        (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), 
        (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)'), 
        (2.0, '5 - 8 человек (до 2,5-х куб.м./ч)'), 
        (2.5, '8 и более человек(от 2,5 - х куб.м./ч)')],
        verbose_name='людей в доме')
    water_hardness = models.BooleanField(verbose_name='жесткость')
    water_ferum = models.BooleanField(verbose_name='железо')
    water_smell = models.BooleanField(verbose_name='запах')
    equipments = models.ManyToManyField(Equipment, through='BaseHouseNoAnalysisEquipment')

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

class BaseHouseNoAnalysisEquipment(models.Model):
    input_data = models.ForeignKey(BaseHouseWithoutWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

    class Meta:
        verbose_name = 'Коттедж --  борудование (нет анализа)'
        verbose_name_plural = verbose_name
        unique_together = ['input_data','equipment']

class CoutryHouseAnalysisEquipment(models.Model):
    
    input_data = models.ForeignKey(CountryHouseWithWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

    class Meta:
        verbose_name = 'Дача --  борудование (есть анализ)'
        verbose_name_plural = verbose_name
        unique_together = ['input_data','equipment']


class CountryHouseNoAnalysisEquipment(models.Model):
    input_data = models.ForeignKey(CountryHouseWithoutWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

    class Meta:
        verbose_name = 'Дача --  борудование (нет анализа)'
        verbose_name_plural = verbose_name
        unique_together = ['input_data','equipment']

class FlatHouseAnalysisEquipment(models.Model):
    
    input_data = models.ForeignKey(FlatHouseWithWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

    class Meta:
        verbose_name = 'Квартира --  борудование (есть анализ)'
        verbose_name_plural = verbose_name
        unique_together = ['input_data','equipment']

class FlatHouseNoAnalysisEquipment(models.Model):
    inout_data = models.ForeignKey(FlatHouseWithoutWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

    class Meta:
        verbose_name = 'Капртира --  борудование (нет анализа)'
        verbose_name_plural = verbose_name
        unique_together = ['inout_data','equipment']
