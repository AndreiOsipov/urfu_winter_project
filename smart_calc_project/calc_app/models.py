from django.db import models
from django.db.models.functions import Length

models.CharField.register_lookup(Length)
def generate_choices(start, end, step):
    choices = []

    for i in range(start, end, step):
        choices.append(
            (i,f'до {i+1}')
        )

    return choices

class BuilderObject(models.Model):

    builder_type = models.CharField(max_length=50, choices=[('H','дом')], verbose_name='Объект')
    montage_place  = models.CharField(max_length=50, choices=[('B', 'бойлерная')], verbose_name='место установки')
    main_water_source = models.CharField(max_length=50,choices=[('W','скважина'),], verbose_name='источник воды')
    sewerage_type = models.CharField(max_length=50, verbose_name='тип каназизации')

    water_consumption = models.FloatField(choices=[(1.2,'до 1,2'),(1.8,'до 1,8'),(2.4,'до 2,4'),(3,'до 3')], verbose_name='потребление воды (л/ч)')
    people_number = models.IntegerField(choices=[(3,'до 3'), (4, 'до 4'), (5, 'до 5'), (6,'до 6'), (7,'до 7')], verbose_name='еоличество человек')
    human_daily_norm = models.FloatField(default=0.15, verbose_name='норма потребления воды на человека в сутки')

    # daily_water_consumption = models.FloatField(verbose_name='общее потребление воды в сутки')
    condensation_protection = models.BooleanField(verbose_name='защита от канденсата')


    def __str__(self) -> str:
        return str(self.water_consumption)
    
    class Meta:
        verbose_name = 'об объекте'
        verbose_name_plural = 'об объектах'


class FullWaterParametrs(models.Model):
    hardness = models.FloatField(choices=generate_choices(0,16,1), verbose_name='жесткость')
    ferum = models.FloatField(choices=generate_choices(0,21, 1),verbose_name='железо')
    po = models.FloatField(choices=generate_choices(0,16,1),verbose_name='ПО')
    hydrogen_sulfite = models.FloatField(choices=generate_choices(0,6,1), verbose_name='сервоводород')
    ammonium = models.FloatField(choices=generate_choices(0,6,1),verbose_name='аммоний')
    manganese = models.FloatField(choices=generate_choices(0,6,1),verbose_name='марганец')

    def __str__(self) -> str:
        return 'жесткость '+str(self.hardness) + 'железо '+ str(self.ferum) +'ПО '+ str(self.po) +'сероводород '+ str(self.hydrogen_sulfite) +'аммоний '+ str(self.ammonium) +'марганец '+ str(self.manganese)

    class Meta:
        verbose_name = 'анализ воды'
        verbose_name_plural = 'анализы воды'

class Columns(models.Model):
    name = models.CharField(max_length=50, verbose_name='название колонны')
    builder_object = models.ForeignKey(BuilderObject, verbose_name='объект, на который она ставится')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'подходящая конна'
        verbose_name_plural = 'подходящие конна'

class Complects(models.Model):
    name = models.CharField(max_length=50, verbose_name='название комплекта')
    full_water_parametrs = models.ForeignKey(FullWaterParametrs, verbose_name='анализ воды')
    builder_object = models.ForeignKey(BuilderObject, verbose_name='объект, с которого взят анализ')
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'комплект оборудования'
        verbose_name_plural = 'комплекы оборудования'

class Equipment(models.Model):
    name = models.CharField(max_length=50, verbose_name='название оборудования')
    price = models.FloatField(verbose_name='цена оборудования')
    complects = models.ManyToManyField(Complects, through='ComplectsEquipments')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'оборудование'
        verbose_name_plural = verbose_name

class ComplectsEquipments(models.Model):
    complect = models.ForeignKey(Complects)
    equipment = models.ForeignKey(Equipment)

class Filler(models.Model):
    name = models.CharField(max_length=50, verbose_name='название наполнителя')
    full_water_parametrs = models.ForeignKey(FullWaterParametrs, verbose_name='полный анализ воды')
    builder_object = models.ForeignKey(BuilderObject, verbose_name='объект, для которого нужен наполнитель')
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'наполнитель'
        verbose_name_plural = 'наполнители'
        
#-----------------------------------------------------------




# class EquipmentType(models.Model):
#     type_name = models.CharField(max_length=50, primary_key=True, verbose_name='тип оборудования')
#     type_discount = models.FloatField(verbose_name='скидка')

#     class Meta:
#         verbose_name = 'Тип оборудования'
#         verbose_name_plural = 'Типы оборудования'

# class Equipment(models.Model):
#     equipment_name = models.CharField(max_length=40, verbose_name='название')
#     equipment_price = models.FloatField(verbose_name='цена')
#     equipment_id = models.CharField(max_length=7, primary_key=True)
#     equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE,verbose_name='Тип оборудования')

#     class Meta:
#         verbose_name = 'Оборудование'
#         verbose_name_plural = verbose_name
#         constraints = [
#             models.CheckConstraint(name='equipment_id_like', check=models.Q(equipment_id__length__gte=7)),
#             models.CheckConstraint(name='price_gte_zero', check=models.Q(equipment_price__gte=0)),            
#         ]
#     def __str__(self) -> str:
#         return self.equipment_name
        
# class AbstractHouse(models.Model): 
#     fiedls_names_for_str = []

#     def get_str_field(self, field):
#         str_field = ''
#         if field.verbose_name:
#             str_field += f'{field.verbose_name} '
#         if field.choices:
#             for choice in field.choices:
#                 if choice[0] == field.value_from_object(self):
#                     str_field+=f'{choice[1]} '
#         else:
#             if field.value_from_object(self):
#                 str_field+='Да '
#             else:
#                 str_field += 'Нет '
#         return str_field

#     def __str__(self) -> str:
#         #прикрепить ->:<-
#         #
#         #
#         str_r = ''
#         for field_name in self.fiedls_names_for_str:
#             field = self._meta.get_field(field_name)
#             str_r += self.get_str_field(field)
#         return str_r

#     class Meta:
#         abstract = True

# class FlatHouseWithWaterAnalysis(AbstractHouse):
#     fiedls_names_for_str = [
#         'water_hardness',
#         'water_ferum',
#         'water_mpc',
#     ]

#     water_hardness = models.IntegerField(choices=[(0, 'до 3'), (3, 'до 7'), (7, 'от 7')], verbose_name='жесткость')
#     water_ferum = models.FloatField(choices=[(0, 'до 0,6'),(0.6, 'до 0,9'), (0.9, 'от 0,9')], verbose_name='железо')
#     water_mpc = models.BooleanField(verbose_name='Другие примеси', blank=True)
#     equipments = models.ManyToManyField(Equipment, through='FlatHouseAnalysisEquipment')

#     class Meta:
#         verbose_name = 'Квартира, есть анализ'
#         verbose_name_plural = verbose_name
#         unique_together = ['water_hardness','water_ferum','water_mpc']

# class CountryHouseWithWaterAnalysis(AbstractHouse):
#     fiedls_names_for_str = [
#         'water_v_used_per_hour',
#         'water_hardness',
#         'water_ferum',
#         'water_mpc',
#         'water_smell',
#     ]
    
#     water_v_used_per_hour = models.FloatField(
#         choices=[
#             (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), 
#             (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)')],
#         verbose_name='людей в доме')
#     water_hardness = models.IntegerField(
#         choices=[
#             (0, 'до 3'),
#             (3, 'до 7'),
#             (7, 'от 7')],
#         verbose_name='жесткость')
#     water_ferum = models.FloatField(
#         choices=[
#             (0, 'до 0,3'),
#             (0.3, 'до 0,9'),
#             (0.9, 'от 0,9')],
#         verbose_name='железо')
    
#     water_mpc = models.BooleanField(verbose_name='другие примеси',blank=True)
#     water_smell = models.BooleanField('запах',blank=True)
#     equipments = models.ManyToManyField(Equipment, through='CoutryHouseAnalysisEquipment')

#     class Meta:
#         verbose_name = 'Дача, есть анализ'
#         unique_together = ['water_v_used_per_hour','water_hardness','water_ferum','water_mpc','water_smell']

# class BaseHouseWithWaterAnalysis(AbstractHouse):
#     fiedls_names_for_str = [
#         'water_v_used_per_hour',
#         'water_hardness',
#         'water_ferum',
#         'water_mpc',
#         'water_smell',
#     ]

#     water_v_used_per_hour = models.FloatField(choices=[
#             (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'),
#             (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)'),
#             (2.0, '5 - 8 человек (до 2,5-х куб.м./ч)'),
#             (2.5, '8 и более человек(от 2,5 - х куб.м./ч)')],
#         verbose_name='людей в доме')
#     water_hardness = models.IntegerField(choices=[
#             (0, 'до 3'),
#             (3, 'до 8'),
#             (8, 'до 15'),
#             (20, 'от 15')], 
#         verbose_name='жесткость')
#     water_ferum = models.FloatField(choices=[
#             (0, 'до 0,3'),
#             (0.3, 'до 0,9'),
#             (0.9, 'до 8'),
#             (8, 'от 8')],
#         verbose_name='железо')
#     water_mpc = models.BooleanField(verbose_name='другие примеси', blank=True)
#     water_smell = models.BooleanField('запах', blank=True)
#     equipments = models.ManyToManyField(Equipment, through='BaseHouseAnalysisEquimpent')
    
#     class Meta:
#         verbose_name = 'Коттедж, есть анализ'
#         verbose_name_plural = verbose_name
#         unique_together = ['water_v_used_per_hour','water_hardness','water_ferum','water_mpc','water_smell']

# class FlatHouseWithoutWaterAnalysis(AbstractHouse):
#     fiedls_names_for_str = [
#         'water_hardness',
#         'water_ferum']
    
#     water_hardness = models.BooleanField(verbose_name='жесткость',default=False)
#     water_ferum = models.BooleanField(verbose_name='железо')    
#     equipments = models.ManyToManyField(Equipment, through='FlatHouseNoAnalysisEquipment')

#     class Meta:
#         verbose_name = 'Квартира, нет анализа'
#         verbose_name_plural = verbose_name
#         unique_together = ['water_hardness','water_ferum']

# class CountryHouseWithoutWaterAnalysis(AbstractHouse):
#     fiedls_names_for_str = [
#         'water_v_used_per_hour',
#         'water_hardness',
#         'water_ferum',
#         'water_smell',
#     ]
    
#     water_v_used_per_hour = models.FloatField(choices=[
#             (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'),
#             (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)')],
#             verbose_name='лидей в доме')
#     water_hardness = models.BooleanField(verbose_name='жесткость')
#     water_ferum = models.BooleanField(verbose_name='железо')
#     water_smell = models.BooleanField(verbose_name='запах', blank=True)
#     equipments = models.ManyToManyField(Equipment, through='CountryHouseNoAnalysisEquipment')

#     class Meta:
#         verbose_name = 'Дача, нет анализа'
#         verbose_name_plural = verbose_name
#         unique_together = ['water_v_used_per_hour', 'water_hardness', 'water_ferum', 'water_smell']

# class BaseHouseWithoutWaterAnalysis(AbstractHouse):
#     fiedls_names_for_str = [
#         'water_v_used_per_hour',
#         'water_hardness',
#         'water_ferum',
#         'water_smell',
#     ]

#     water_v_used_per_hour = models.FloatField(choices=[
#         (1.0, '1 - 2 человека (до 1,3 куб.м./ч)'), 
#         (1.3, ' 3 - 4 человека (до 2-х куб.м./ч)'), 
#         (2.0, '5 - 8 человек (до 2,5-х куб.м./ч)'), 
#         (2.5, '8 и более человек(от 2,5 - х куб.м./ч)')],
#         verbose_name='людей в доме')
    
#     water_hardness = models.BooleanField(verbose_name='жесткость')
#     water_ferum = models.BooleanField(verbose_name='железо')
#     water_smell = models.BooleanField(verbose_name='запах', blank=True)
#     equipments = models.ManyToManyField(Equipment, through='BaseHouseNoAnalysisEquipment')

#     class Meta:
#         verbose_name = 'Коттедж, нет анализа'
#         verbose_name_plural = verbose_name
#         unique_together = ['water_v_used_per_hour', 'water_hardness', 'water_ferum', 'water_smell']

# class BaseHouseAnalysisEquimpent(models.Model):
#     input_data = models.ForeignKey(BaseHouseWithWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
#     equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')
    
#     class Meta:
#         verbose_name = 'Коттедж --  борудование (есть анализ)'
#         verbose_name_plural = verbose_name
#         unique_together = ['input_data','equipment']

# class BaseHouseNoAnalysisEquipment(models.Model):
#     input_data = models.ForeignKey(BaseHouseWithoutWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
#     equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

#     class Meta:
#         verbose_name = 'Коттедж --  борудование (нет анализа)'
#         verbose_name_plural = verbose_name
#         unique_together = ['input_data','equipment']

# class CoutryHouseAnalysisEquipment(models.Model):
    
#     input_data = models.ForeignKey(CountryHouseWithWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
#     equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

#     class Meta:
#         verbose_name = 'Дача --  борудование (есть анализ)'
#         verbose_name_plural = verbose_name
#         unique_together = ['input_data','equipment']


# class CountryHouseNoAnalysisEquipment(models.Model):
#     input_data = models.ForeignKey(CountryHouseWithoutWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
#     equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

#     class Meta:
#         verbose_name = 'Дача --  борудование (нет анализа)'
#         verbose_name_plural = verbose_name
#         unique_together = ['input_data','equipment']

# class FlatHouseAnalysisEquipment(models.Model):
    
#     input_data = models.ForeignKey(FlatHouseWithWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
#     equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

#     class Meta:
#         verbose_name = 'Квартира --  борудование (есть анализ)'
#         verbose_name_plural = verbose_name
#         unique_together = ['input_data','equipment']

# class FlatHouseNoAnalysisEquipment(models.Model):
#     inout_data = models.ForeignKey(FlatHouseWithoutWaterAnalysis, on_delete=models.CASCADE, verbose_name='входные данные')
#     equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')

#     class Meta:
#         verbose_name = 'Капртира --  борудование (нет анализа)'
#         verbose_name_plural = verbose_name
#         unique_together = ['inout_data','equipment']