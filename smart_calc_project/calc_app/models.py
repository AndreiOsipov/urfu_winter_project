from django.db import models
from django.db.models.functions import Length
from .genereator_for_fields import ChoicesGenerator
models.CharField.register_lookup(Length)


class Admixture(models.Model):
    name = models.CharField(max_length=20, verbose_name='название')
    exceeding_consecuences = models.TextField(verbose_name='последствия превышения')
    recommendations = models.TextField(verbose_name='рекомендации')
    criitical_value = models.FloatField(verbose_name='критическое значение')

    class Meta:
        verbose_name = 'Примесь'
        verbose_name_plural = 'Примеси'

class WaterConsumptionLevel(models.Model):
    water_consumption = models.FloatField(choices=[
        (1.2,'до 1,2 3 точки (пример: 2 крана и душ)'),
        (1.8,'до 1,8 4-5 точек (пример: 2 крана, стиральная машина/посудомоечная машина, душ) (пиктограммами)'),
        (2.4,'до 2,4 4-5 точек большего объема (пример: 2 крана, стиральная машина и посудомоечная машина, тропический душ)'),
        (3,'до 3 от 5 точки большего объема (пример: бассейн, или 2 крана, стиральная машина и посудомоечная машина, тропический душ)')
        ], verbose_name='потребление воды (л/ч)')
    people_number = models.IntegerField(choices=[(3,'до 3'), (4, 'до 4'), (5, 'до 5'), (6,'до 6'), (7,'до 7')], verbose_name='еоличество человек')
    human_daily_norm = models.FloatField(default=0.15, verbose_name='норма потребления воды на человека в сутки')

    @property
    def dayly_consumption(self):
        return self.human_daily_norm * self.people_number
    class Meta:
        verbose_name = 'Уровень потреьоения воды'
        verbose_name_plural = 'уровни потребления воды'

class FullWaterParametrs(models.Model):
    choices_generator = ChoicesGenerator()
    hardness = models.FloatField(choices=choices_generator.generate_choices(0,16,1), verbose_name='жесткость')
    ferum = models.FloatField(choices=choices_generator.generate_choices(0,21, 1),verbose_name='железо')
    po = models.FloatField(choices=choices_generator.generate_choices(0,16,1),verbose_name='ПО')
    hydrogen_sulfite = models.FloatField(choices=choices_generator.generate_choices(0,6,1), verbose_name='сервоводород')
    ammonium = models.FloatField(choices=choices_generator.generate_choices(0,6,1),verbose_name='аммоний')
    manganese = models.FloatField(choices=choices_generator.generate_choices(0,6,1),verbose_name='марганец')
    

#filter vs get ?

    @property
    def get_default_hardness_exceeding(self):
        hardness_admixture = Admixture.objects.filter(name='жесткость').first()
        if not (hardness_admixture is None):
            return hardness_admixture.pk
    
    @property
    def get_default_ferum_exceeding(self):
        ferum_admixture = Admixture.objects.filter(name='железо').first()
        if not (ferum_admixture is None):
            return ferum_admixture.pk

    @property
    def get_default_hydrogen_sulfite_exceeding(self):
        hydrogen_admixture = Admixture.objects.filter(name='сероводород').first()
        if not(hydrogen_admixture is None):
            return hydrogen_admixture.pk
        
    @property
    def get_default_ammonium_exceeding(self):
        ammonium_admixture = Admixture.objects.filter(name='аммоний').first()
        if not(ammonium_admixture is None):
            return ammonium_admixture.pk
    
    @property
    def get_default_manganese_exceeding(self):
        manganese_admixture = Admixture.objects.filter(name='марганец').first()
        if not(manganese_admixture is None):
            return manganese_admixture.pk
    
    @property
    def get_default_po_exceeding(self):
        po_admixture = Admixture.objects.filter(name='по').first()
        if not(po_admixture is None):
            return po_admixture.pk
    



    # exceeding_consequence = models.TextField(blank=True, verbose_name='последстваия превышения')
    # recommendations = models.TextField(blank=True, verbose_name='рекоммендации')
    
    def __str__(self) -> str:
        return 'жесткость '+str(self.hardness) + 'железо '+ str(self.ferum) +'ПО '+ str(self.po) +'сероводород '+ str(self.hydrogen_sulfite) +'аммоний '+ str(self.ammonium) +'марганец '+ str(self.manganese)

    class Meta:
        verbose_name = 'анализ воды'
        verbose_name_plural = 'анализы воды'

class Columns(models.Model):
    name = models.CharField(max_length=50, verbose_name='название колонны')
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'водяная колонна'
        verbose_name_plural = 'водяные колонны'

class Complects(models.Model):
    
    full_water_parametrs = models.ForeignKey(FullWaterParametrs, on_delete=models.CASCADE, verbose_name='анализ воды')
    water_consumption_level = models.ForeignKey(WaterConsumptionLevel, verbose_name='уровень потребления воды', on_delete=models.CASCADE)
    column = models.ForeignKey(Columns, verbose_name='колонна', on_delete=models.CASCADE)

    complect_code = models.CharField(max_length=250, verbose_name='код комплекта')
    name = models.CharField(max_length=50, verbose_name='название комплекта')
    photo = models.ImageField(verbose_name='фото комплекта', null=True)
    discrpiption = models.TextField(verbose_name='описание комплекта')

    max_system_performans = models.FloatField(verbose_name='максимальная производительность системы (м3 / ч)')
    min_pressure = models.FloatField(verbose_name='Давление воды на входе системы водоподготовки минимальное, при максимальном расходе м3/час, атм.')
    max_pressure = models.FloatField(verbose_name='Давление воды на входе системы водоподготовки максимальное, атм.')
    pressure_loss = models.FloatField(verbose_name='Потери давления в системе, атм.')
    body_life_time = models.IntegerField(verbose_name='Срок эксплуатации корпусов фильтров, лет')
    regenerations_loss_v = models.FloatField(verbose_name='Объем воды, сбрасываемой многофункциональным фильтром во время регенерации, м3')
    regeneration_period = models.CharField(max_length= 50,verbose_name='Периодичность регенерации')

    min_size = models.CharField(max_length=50, verbose_name='Минимальные размеры для установки, м')
    min_hight = models.FloatField(verbose_name='Минимальная высота потолка, м')
    sockets_number = models.IntegerField(verbose_name='Наличие электрических розеток, со стабилизированным U ~ 220В 10%, шт., не менее	1')
    electric_power = models.IntegerField(verbose_name='Общая электрическая мощность системы водоподготовки, Вт	25')
    doorways_size  = models.CharField(max_length = 50, verbose_name='Дверные проемы, мм')
    requered_flat_floor_cover = models.BooleanField(verbose_name='Наличие ровного полового покрытия в месте установки водоподготовки')
    required_ventilation = models.BooleanField(verbose_name='Наличие в помещении приточной и вытяжной вентиляции')
    required_severage = models.BooleanField(verbose_name='Наличие канализационной сети в месте установки водоподготовки	обязательно')
    severage_d = models.CharField(max_length=50,verbose_name='Диаметр канализационной сети в месте врезки регенерационной линии с фильтров')

    condensation_protection = models.BooleanField(verbose_name='защита от канденсата')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'комплект оборудования'
        verbose_name_plural = 'комплекы оборудования'

class EquipmentType(models.Model):
    name = models.CharField(max_length=50,verbose_name='название типа')

    class Meta:
        verbose_name = 'тип оборудования'
        verbose_name_plural = 'типы оборудования'

class Equipments(models.Model):
    name = models.CharField(max_length=50, verbose_name='название оборудования')
    price = models.FloatField(verbose_name='цена оборудования')
    complects = models.ManyToManyField(Complects, through='ComplectsEquipments')
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'оборудование'
        verbose_name_plural = verbose_name

class ComplectsEquipments(models.Model):
    complect = models.ForeignKey(Complects, on_delete=models.CASCADE, related_name='complects_equipments')
    equipment = models.ForeignKey(Equipments, on_delete=models.CASCADE,related_name='equipments_complects')
    class Meta:
        verbose_name = 'принадлежность оборудования к комплекту'
        verbose_name_plural = 'принадлежность оборудования к комплектам'

class Fillers(models.Model):
    full_water_parametrs = models.ForeignKey(FullWaterParametrs, verbose_name='полный анализ воды', on_delete=models.CASCADE)
    water_consumption_level = models.ForeignKey(WaterConsumptionLevel, verbose_name='уровень потребления воды', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='название наполнителя')
    price = models.FloatField(verbose_name= 'цена наполнителя', default=500)
    
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'наполнитель'
        verbose_name_plural = 'наполнители'

class BuilderObject(models.Model):

    builder_type = models.CharField(max_length=50, choices=[('H','дом')], verbose_name='Объект')
    montage_place  = models.CharField(max_length=50, choices=[('B', 'бойлерная')], verbose_name='место установки')
    main_water_source = models.CharField(max_length=50,choices=[('W','скважина'),], verbose_name='источник воды')
    sewerage_type = models.CharField(max_length=50, verbose_name='тип каназизации')

    def __str__(self) -> str:
        return str(self.builder_type)
    
    
    class Meta:
        verbose_name = 'об объекте'
        verbose_name_plural = 'об объектах'

class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class MontageWork(models.Model):
    complects = models.ManyToManyField(Complects, through='ComplectMontage')
    name = models.CharField(max_length=50,verbose_name='название')
    price = models.FloatField(verbose_name='цена')

class ComplectMontage(models.Model):
    montage_work = models.ForeignKey(MontageWork, on_delete=models.CASCADE)
    complect = models.ForeignKey(Complects, on_delete=models.CASCADE)

class Contract(models.Model):
    equipments = models.ManyToManyField(Equipments, through='ContractEquipment')
    fillers = models.ManyToManyField(Fillers, verbose_name='наполнители', through='ContractFillers')
    montage_works = models.ManyToManyField(MontageWork, through='ContractMontageWork')
    complect = models.ForeignKey(Complects, verbose_name='комплект', on_delete=models.CASCADE)
    # complect = models.ManyToManyField(Complects, verbose_name='комплекты к этому договору', through='ContractComplect')
    client = models.ForeignKey(Client, verbose_name='клиент', on_delete=models.CASCADE)
    builder_obj = models.ForeignKey(BuilderObject, verbose_name='объект, для которого подобрали фильры', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'договоры'

# class ContractComplect(models.Model):
#     contract = models.ForeignKey(Contract, verbose_name='договор', on_delete=models.CASCADE)
#     complect = models.ForeignKey(Complects, verbose_name='комплект', on_delete=models.CASCADE)

class ContractMontageWork(models.Model):
    contract = models.ForeignKey(Contract,verbose_name='договор', on_delete=models.CASCADE)
    montage_work = models.ForeignKey(MontageWork, verbose_name='работа', on_delete=models.CASCADE)
    number = models.IntegerField()
    montage_price_for_this_contract = models.FloatField()

    @property 
    def cost(self):
        return self.number * self.montage_price_for_this_contract


class ContractFillers(models.Model):
    contract = models.ForeignKey(Contract, verbose_name='договор', on_delete=models.CASCADE)
    filler = models.ForeignKey(Fillers, verbose_name='наполнитель', on_delete=models.CASCADE)


class ContractEquipment(models.Model):
    choice_generator = ChoicesGenerator()
    equipment = models.ForeignKey(Equipments,verbose_name='оборудование', on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract,verbose_name='контракт', on_delete=models.CASCADE)
    number = models.IntegerField(choices=choice_generator.generate_choices(1, 4, 1))
    equipment_price_for_this_contract = models.FloatField()
    
    @property 
    def cost(self):
        return self.number * self.equipment_price_for_this_contract

    class Meta:
        verbose_name =  'прайс-лсит на этот договор'
        verbose_name_plural = 'прайс-листы к договорам'