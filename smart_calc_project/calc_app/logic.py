class FinalOffer:
    '''
    содержит id всех фильтров и наполнителей + id доп.предложений
    '''
    def __init__(self, equipments, kitchen_filters, fillers, extra_equipments) -> None:
        self.main_equipments = equipments
        self.kitchen_filters = kitchen_filters
        self.fillers = fillers
        self.extra_offers = extra_equipments
    def __str__(self) -> str:
        return f'main_equimpents: {self.main_equipments}\nkitchen: {self.kitchen_filters}\
        \nfillers: {self.fillers}\nextra_offers: {self.extra_offers}'
class FillerInfo:
    '''
    представляет наполнитель
    поле id -- представляет поле в таблице, по которому будет искаться вид наполнителя
    у разных экземпляров может быть одинаковый id, но разный объем и цена
    '''
    def __init__(self, filler_id, filler_v, filler_price) -> None:
        self.id = filler_id
        self.v = filler_v
        self.price = filler_price

class ExtraWaterParametrs:
    '''
    дополнительные параметры воды
    any -- флаг, ознчающий, что комбинация будет выбрана при превышении ПДК любого показателя 
    '''
    def __init__(self, turbidity=0.0, ph=0.0, oxid=0.0, nitrat=0.0, salt=0.0, nitrit=0.0, color=0.0, any=False) -> None:
        self.turbidity = turbidity
        self.ph = ph
        self.oxid = oxid
        self.nitrat = nitrat
        self.salt = salt
        self.nitrit = nitrit
        self.color = color
        self.any = any

class WaterCheckerWithValues:
    def __init__(self, hard: tuple,ferum : tuple, extra_water_parametrs=ExtraWaterParametrs(), smell=False) -> None:
        self.ferum_begin = ferum[0]
        self.ferum_end = ferum[1]
        self.hard_begin = hard[0]
        self.hard_end = hard[1]
        self.extra_water_parametrs = extra_water_parametrs
        self.smell = smell
    def __str__(self) -> str:
        return f'ferum: {self.ferum_begin} -- {self.ferum_end}\nhard: {self.hard_begin} -- {self.hard_end}\
        \nany: {self.extra_water_parametrs.any}\nsmell: {self.smell}'
    def check(self, water_hardness, water_ferum,water_mpc, smell=False):
        '''
        первая проверка на налиие запаха
        вторая проверка на наличие доп. параметров загрязнения, если они есть возвращается значение any из
        поля extra_water_parametrs
        если нету ни запаха ни дополнительных примесей, идет стандартная проверка на железо и жжесткость
        '''
        if smell:
            return self.smell

        for extra_parametr_name in water_mpc.keys():
            if water_mpc[extra_parametr_name] > 1:
                return self.extra_water_parametrs.any

        return (water_ferum >= self.ferum_begin and water_ferum < self.ferum_end)\
            and (water_hardness >= self.hard_begin and water_hardness < self.hard_end)

class WaterCheckerWithoutValues:
    def __init__(self, hardness: bool, ferum: bool, smell=False) -> None:
        self.hardness = hardness
        self.ferum = ferum
        self.smell = smell

    def check(self, water_hardness, water_ferum, water_mpc, smell=False):
        if smell:
            return self.smell
        return self.ferum == water_ferum and self.hardness == water_hardness


class Logic:
    '''
    основной класс логики
    хранит у себя экземпляры вариантов наполнителей
    каждый экзепляр представляет вид наполнителя определенного объема с ценой ха этот объем
    и логические словари
    где ключи -- экземпляры класса WaterCheckerWithValues или WaterCheckerWithoutValues
    а значения -- списки с id оборудования и экземплярами наполнителей,
    упаковынные в другие структуры (словари, списки) в соответсвии с таблицей
    извлечение информации происходит сначала проверкой, что данные анализа воды соответсвуют чекеру,
    после чего из из значения словаря извлекается вся нужная информация
    '''
    EM_25 = FillerInfo('EM0001', 25, 5)
    EM_50 = FillerInfo('EM0001', 50, 10)
    EM_60 = FillerInfo('EM0001', 62.5, 13)
    EM_80 = FillerInfo('EM0001', 80, 17)
    EMP_50 = FillerInfo('EM0002', 50, 4)
    EMP_62 = FillerInfo('EM0002', 62.5, 5)
    EMP_80 = FillerInfo('EM0002', 80, 18)
    EMC_25 = FillerInfo('EM0003', 25, 9)
    EMC_50 = FillerInfo('EM0003', 50, 10)
    EMC_62 = FillerInfo('EM0003', 62.5, 15)
    EMC_80 = FillerInfo('EM0003', 80, 20)
    SM_25 = FillerInfo('SM0000', 25, 15)
    SM_50 = FillerInfo('SM0000', 50, 17)
    SM_62 = FillerInfo('SM0000', 62.5, 20)
    SM_80 = FillerInfo('SM0000', 80, 25)
    FM_25 = FillerInfo('FM0000', 25, 10)
    FM_50 = FillerInfo('FM0000', 50, 20)
    FM_62 = FillerInfo('FM0000', 62.5, 25)
    FM_80 = FillerInfo('FM0000', 80, 30)
    SA_50 = FillerInfo(
        'SA0000', 50, 12)
    ABS_MAX = 100

    HOUSE_BASE_LOGIC_DICT = {
        #каждое значение -- одна строка таблицы(список)
        #длина списка -- 4 (возможные варианты количества людей в доме)
        #на каждом месте в списке по словарю,
        #словарь хранти ключи (main_filters_components, kitchen_filters, fillers) -- и соответствующие оборудование в списках

        WaterCheckerWithValues((0, 3), (0, 0.3)): [
                    #ВВ0020 - BB20 (Карбон-блок)
                    #ВВ0021 - BB20 (Феронить)
                    #BBP020 - BB20 (Посткарбон)
                    #ES0000 - Expert Standart 
                    #PR0111 - Профи Осмо
                    #WF0111 - Барьер Waterfort
                    #EC0000 - Expert Complex
                    #EX0000 - Expert смягчение
                    #KL1044 - Колонна 1044
                    #KL1252 - Колонна 1252
                    #KL1354 - Колонна 1354
                    #KL1465 - Колонна 1465
                    #BU0034 - Блок управления 100v3/4
                    #BU1001 - Блок управления 100V1 
                    #EM0001 - Ecomix A (25л)
                    #EM0052 - Ecomix P (50л)
                    #EM0062 - Ecomix P (62,5л) 
                    #EM0080 - Ecomix P (80л)
                    #EM0051 - Ecomix C (50л)
                    #EM0063 - Ecomix C (62,5л)
                    #EM0081 - Ecomix C (80л)
                    #SM0025 - Softmix (25л)
                    #SM0050 - Softmix (50л)
                    #SM0062 - Softmix (62,5л)
                    #SM0080 - Softmix (80л)
                    #FM0050 - Ferromix (50)
                    #FM0062 - Ferromix (62,5)
                    #FM0080 - Ferromix (80)
                    #BA0100 - Колонна аэрации Barier Aero Pro 100
                    #KG0050 - 50 кг соли
                    #SB0000 - Солевой бак 
                    #BBK200 -- корпус BB20(механический картиридж)
                    #BB0010 -- bb10 карбон-блок
                    #BB0110 -- BB10 (механика)
                    #BB0120 -- BB20 (механика)
                    #PR1111 -- m
                    #BB0011 -- bb10 ферронить
                    #BB0012 -- bb10 смягчение
                    #BB0022 -- bb20 смягчение
                    #EH0000 -- expert hard
                    #EH0002 -- 2xexpert hard
                    #BB0023 -- BB20 механника (грязивик)
                    #PR0000 -- Protector x/в
                    #PR0001 -- Protector r/в
                    #SL0000 -- Softline | специальная очистка
                    #FD0000 -- FDD | специальная очистка
                   {'main_filters_components': ['BB0020'], 'kitchen_filters': ['ES0000', 'PR0111', 'WF0111'], 'fillers':[]},
                    {'main_filters_components': ['BB0020'], 'kitchen_filters': ['ES0000', 'PR0111', 'WF0111'], 'fillers': []},
                    {'main_filters_components': ['BB0020'], 'kitchen_filters': ['ES0000', 'PR0111', 'WF0111'], 'fillers': []},
                    {'main_filters_components': ['BB0020'], 'kitchen_filters': ['ES0000', 'PR0111', 'WF0111'], 'fillers': []}
                    ],
        WaterCheckerWithValues((0, 3), (0.3, 0.9)): [
                    {'main_filters_components': ['BB0021'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers': []},
                    {'main_filters_components': ['KL1044', 'BU0034', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_25, SA_50]},
                    {'main_filters_components': ['KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_25, SA_50]},
                    {'main_filters_components': ['KL1465', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_80, SA_50]}
                    ],
        WaterCheckerWithValues((0, 3), (0.9, 8)): [
                    {'main_filters_components': ['KL1044', 'BU0034', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_25, SA_50]},
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_50, SA_50]},
                    {'main_filters_components': ['KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EMC_62, SA_50]},
                    {'main_filters_components': ['KL1465', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EMC_80, SA_50]}
                    ],
        WaterCheckerWithValues((3, 8), (0, 0.3)): [
                    {'main_filters_components': ['KL1044', 'BU0034', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers':[SM_25, SA_50]},
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers':[SM_50, SA_50]},
                    {'main_filters_components': ['KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers':[SM_62, SA_50]},
                    {'main_filters_components': ['KL1465', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers':[SM_80, SA_50]}
                    ],
        WaterCheckerWithValues((3, 8), (0.3, 8)): [
                    {'main_filters_components': ['KL1044', 'BU0034', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_25, SA_50]},
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000',  'PR0111', 'WF0111'], 'fillers':[EM_50, SA_50]},
                    {'main_filters_components': ['KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_60, SA_50]},
                    {'main_filters_components': ['KL1465', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_80, SA_50]}
                    ],
        WaterCheckerWithValues((8, 15), (0, 0.3)): [
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers': [SM_50, SA_50]},
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers': [SM_50, SA_50]},
                    {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []},
                    {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []}
                    ],
        WaterCheckerWithValues((8, 15), (0.3, 8)): [
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers': [EM_50, SA_50]},
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020', 'KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers': [EMC_50, SA_50, EM_60, SA_50]},
                    {'main_filters_components': ['KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': [], 'fillers': [EM_50, SA_50, EM_60, SA_50]},
                    {'main_filters_components': ['KL1465', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': [], 'fillers': [EM_50, SA_50, EM_80, SA_50]}
                    ],
        WaterCheckerWithValues((8, 15),(8, ABS_MAX)): [
                    {'main_filters_components': ['BA0100', 'KL1252', 'FM0050', 'KL1252', 'SB0000', 'BB0020'], 'kitchen_filters': [], 'fillers': [EMP_50, SA_50]},
                    {'main_filters_components': ['BA0100', 'KL1354', 'FM0062', 'KL1354', 'SB0000', 'BB0020'], 'kitchen_filters': [], 'fillers': [EMP_62, SA_50]},
                    {'main_filters_components': ['BA0100', 'KL1354', 'FM0062', 'KL1354', 'SB0000', 'BB0020'], 'kitchen_filters': [], 'fillers': [EMP_62, SA_50]},
                    {'main_filters_components': ['BA0100', 'KL1465', 'FM0080', 'KL1465', 'SB0000', 'BB0020'], 'kitchen_filters': [], 'fillers': [EM_80, SA_50]}
                    ],
        WaterCheckerWithValues((15, ABS_MAX),(8, ABS_MAX)): [
                    {'main_filters_components': ['BA0100', 'KL1252', 'FM0050', 'KL1252', 'SB0000', 'BB0020'], 'kitchen_filters': [], 'fillers': [EMC_50, SA_50]},
                    {'main_filters_components': ['BA0100', 'KL1354', 'FM0062', 'KL1354', 'SB0000', 'BB0020'], 'kitchen_filters': [], 'fillers': [EMP_62, SA_50]},
                    {'main_filters_components': ['BA0100', 'KL1354', 'FM0062', 'KL1354', 'SB0000', 'BB0020'], 'kitchen_filters': [], 'fillers': [EMP_62, SA_50]},
                    {'main_filters_components': ['BA0100', 'KL1465', 'FM0080', 'KL1465', 'SB0000', 'BB0020'], 'kitchen_filters': [], 'fillers': [EM_80, SA_50]}
                    ],
        WaterCheckerWithValues((0, ABS_MAX), (0, ABS_MAX), extra_water_parametrs=ExtraWaterParametrs(any=True)):[
            {'main_filters_components': ['BBK200', 'KL1044', 'SB0000', 'BB0020'], 'fillers': [EMC_25, SA_50], 'kitchen_filters':[]},
            {'main_filters_components': ['BBK200', 'KL1252', 'SB0000', 'BB0020'], 'fillers': [EMC_50, SA_50], 'kitchen_filters': []},
            {'main_filters_components': ['BBK200', 'KL1354','BU1001', 'SB0000', 'BB0020'], 'fillers': [EMC_62, SA_50], 'kitchen_filters':[]},
            {'main_filters_components': ['BBK200', 'KL1465','BU1001', 'SB0000', 'BB0020'], 'fillers': [EMC_80, SA_50], 'kitchen_filters':[]}],
        WaterCheckerWithValues((0, ABS_MAX),(0, ABS_MAX),smell=True): [
            {'main_filters_components': ['BA0100', 'KL1044', 'KL1044', 'SB0000', 'BB0020'], 'fillers': [EMC_25, FM_25, SA_50], 'kitchen_filters':[]},
            {'main_filters_components': ['BA0100', 'KL1252', 'KL1252', 'SB0000', 'BB0020'], 'fillers': [EMC_50, FM_50, SA_50], 'kitchen_filters':[]},
            {'main_filters_components': ['BA0100', 'KL1354', 'KL1354', 'SB0000', 'BB0020'], 'fillers': [EMC_62, FM_62, SA_50], 'kitchen_filters':[]},
            {'main_filters_components': ['BA0100', 'KL1465', 'KL1465', 'SB0000', 'BB0020'], 'fillers': [EMC_80, FM_80, SA_50], 'kitchen_filters':[]}]}

    HOUSE_BASE_LOGIC_DICT_WITHOUT_VALUES = {
        WaterCheckerWithoutValues(False, False, False): [
        {'main_filters_components':['BB0020'], 'kitchen_filters':['ES0000','PR0111','WF0111'], 'fillers': []},
        {'main_filters_components':['BBP020'], 'kitchen_filters':['ES0000','PR0111','WF0111'], 'fillers': []},
        {'main_filters_components':['BBP020'], 'kitchen_filters':['ES0000','PR0111','WF0111'], 'fillers': []},
        {'main_filters_components':['BBP020'], 'kitchen_filters':['ES0000','PR0111','WF0111'], 'fillers': []}],
        WaterCheckerWithoutValues(False, True, False): [
            {'main_filters_components':['KL1044','BU0034','SM0000','BB0020'],'kitchen_filters':['EC0000','PR0111','WF0111'],'fillers':[EMC_25,SA_50]},
            {'main_filters_components':['KL1252','BU0101','SM0000','BB0020'],'kitchen_filters':['EC0000','PR0111','WF0111'],'fillers':[EMC_50,SA_50]},
            {'main_filters_components':['KL1354','BU0101','SM0000','BB0020'],'kitchen_filters':['EC0000','PR0111','WF0111'],'fillers':[EMP_62,SA_50]},
            {'main_filters_components':['KL1465','BU0101','SM0000','BB0020'],'kitchen_filters':['EC0000','PR0111','WF0111'],'fillers':[EMP_80,SA_50]}],
        WaterCheckerWithoutValues(True, False, False): [
            {'main_filters_components': ['KL1044', 'BU0034', 'SB0000', 'BB0020'], 'kitchen_filters':['EH0002','PR0111','WF0111'], 'fillers':[SM_25, SA_50]},
            {'main_filters_components': ['KL1252', 'BU0101', 'SB0000', 'BB0020'], 'kitchen_filters':['EH0002','PR0111','WF0111'], 'fillers':[SM_50, SA_50]},
            {'main_filters_components': ['KL1354', 'BU0101', 'SB0000', 'BB0020'], 'kitchen_filters':['EH0002','PR0111','WF0111'], 'fillers':[SM_62, SA_50]},
            {'main_filters_components': ['KL1465', 'BU0101', 'SB0000', 'BB0020'], 'kitchen_filters':['EH0002','PR0111','WF0111'], 'fillers':[SM_80, SA_50]}
        ],    
        WaterCheckerWithoutValues(True, True, False): [
            {'main_filters_components':['KL1044','BU0034','SB0000','BB0020'],'kitchen_filters':['EC0000','PR0111','WF0111'],'fillers':[EMC_25, SA_50]},
            {'main_filters_components':['KL1252','BU101','SB0000','BB0020'],'kitchen_filters':['EC0000','PR0111','WF0111'],'fillers':[EMC_50, SA_50]},
            {'main_filters_components':['KL1354','BU0101','SB0000','BB0020'],'kitchen_filters':['EC0000','PR0111','WF0111'],'fillers':[EMC_62, SA_50]},
            {'main_filters_components':['KL1465','BU0034','SB0000','BB0020'],'kitchen_filters':['EC0000','PR0111','WF0111'],'fillers':[EMC_80, SA_50]}
        ],
        WaterCheckerWithoutValues(True, True, True):[
            {'main_filters_components':['BA0100', 'KL1044', 'KL1044', 'SB0000', 'BB0020'], 'fillers': [FM_25, EMC_25, SA_50], 'kitchen_filters':[]},
            {'main_filters_components':['BA0100', 'KL1252', 'KL1252', 'SB0000', 'BB0020'], 'fillers': [FM_50, EMC_50, SA_50], 'kitchen_filters':[]},
            {'main_filters_components':['BA0100', 'KL1354', 'KL1354', 'SB0000', 'BB0020'], 'fillers': [FM_62, EMC_62, SA_50], 'kitchen_filters':[]},
            {'main_filters_components':['BA0100', 'KL1465', 'KL1465', 'SB0000', 'BB0020'], 'fillers': [FM_80, EMC_80, SA_50], 'kitchen_filters':[]}
        ]
    }
    

    COUNTRY_HOUSE_LOGIC_DICT = {
        WaterCheckerWithValues((0, 3), (0, 0.3)) : [
            {'main_filters_components': ['BB0010'], 'kitchen_filters': ['ES0000', 'PR0111', 'PR1111'], 'fillers': []},
            {'main_filters_components': ['BB0020'], 'kitchen_filters': ['ES0000', 'PR0111', 'PR1111'], 'fillers': []}
        ],
        WaterCheckerWithValues((0, 3), (0.3, 0.9)) : [
            {'main_filters_components': ['BB0010'], 'kitchen_filters': ['EC0000', 'PR0111', 'PR1111'], 'fillers': []},
            {'main_filters_components': ['BB0021'], 'kitchen_filters': ['EC0000', 'PR0111', 'PR1111'], 'fillers': []}],
        WaterCheckerWithValues((3, 7), (0, 0.3)) : [
            {'main_filters_components': ['BB0022'], 'kitchen_filters': ['ES0000', 'PR0111', 'PR1111'], 'fillers': []},
            {'main_filters_components': ['BB0022'], 'kitchen_filters': ['ES0000', 'PR0111', 'PR1111'], 'fillers': []}
            ],
        WaterCheckerWithValues((3, 7), (0.3, 0.9)) : [
            {'main_filters_components': ['BB0011', 'BB0022'], 'kitchen_filters': ['EC0000', 'PR0111', 'PR1111'], 'fillers': []},
            {'main_filters_components': ['BB0021', 'BB0022'], 'kitchen_filters': ['EC0000', 'PR0111', 'PR1111'], 'fillers': []}
            ],
        WaterCheckerWithValues((7, ABS_MAX), (0, 0.9)):[
            {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []},
            {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []}],
            WaterCheckerWithValues((0, 7), (0.9, ABS_MAX)):[
            {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []},
            {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []}],
            WaterCheckerWithValues((7, ABS_MAX), (0.9, ABS_MAX)):[
            {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []},
            {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []}],
         WaterCheckerWithValues((0, ABS_MAX),(0, ABS_MAX), ExtraWaterParametrs(any=True)):[
            {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []},
            {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []}
         ],
         WaterCheckerWithValues((0, ABS_MAX),(0, ABS_MAX),smell=True):[
            {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []},
            {'main_filters_components': [], 'kitchen_filters': [], 'fillers': []}
         ]}
    COUNTRY_HOUSE_LOGIC_DICT_WITHOUT_VALUES = {
        WaterCheckerWithoutValues(False, False):[
        {'main_filters_components':['BB0010'], 'kitchen_filters': ['ES0000','PR0111','PR1111'], 'fillers': []},
        {'main_filters_components':['BB0020'], 'kitchen_filters': ['ES0000','PR0111','PR1111'], 'fillers': []}],
        WaterCheckerWithoutValues(False, True):[
        {'main_filters_components':['BB0011'], 'kitchen_filters': ['EC0000','PR0111','PR1111'], 'fillers': []},
        {'main_filters_components':['BB0021'], 'kitchen_filters': ['EC0000','PR0111','PR1111'], 'fillers': []}],
        WaterCheckerWithoutValues(True, False):[
        {'main_filters_components':['BB0022'], 'kitchen_filters': ['ES0000','PR0111','PR1111'], 'fillers': []},
        {'main_filters_components':['BB0022'], 'kitchen_filters': ['ES0000','PR0111','PR1111'], 'fillers': []}],
        WaterCheckerWithoutValues(True, True):[
        {'main_filters_components':['BB0011', 'BB0012'], 'kitchen_filters': ['EC0000','PR0111','PR1111'], 'fillers': []},
        {'main_filters_components':['BB0021', 'BB0022'], 'kitchen_filters': ['EC0000','PR0111','PR1111'], 'fillers': []}],
        WaterCheckerWithoutValues(True, True, True):[
        {'main_filters_components':[], 'kitchen_filters': [], 'fillers': []},
        {'main_filters_components':[], 'kitchen_filters': [], 'fillers': []}],
    }

    FLAT_LOGIC_DICT = {
        WaterCheckerWithValues((0, 3),(0, 0.6)): ['ES0000'],
        WaterCheckerWithValues((0, 3),(0.6, 0.9)): ['EC0000', 'PR0111', 'PR1111'],
        WaterCheckerWithValues((3, 7),(0, 0.6)): ['EH0000', 'PR0111', 'PR1111'],
        WaterCheckerWithValues((3, 7),(0.6, 0.9)): ['EC0000', 'PR0111', 'PR1111'],
        WaterCheckerWithValues((7, ABS_MAX),(0.6, 0.9)): ['PR0111', 'PR1111'],
        WaterCheckerWithValues((3, 7),(0.9, ABS_MAX)): ['PR0111', 'PR1111'],
        WaterCheckerWithValues((7, ABS_MAX),(0.9, ABS_MAX)): ['PR0111', 'PR1111'],
        WaterCheckerWithValues((7, ABS_MAX),(0.9, ABS_MAX), ExtraWaterParametrs(any=True)): ['PR0111', 'PR1111']}

    FLAT_LOGIC_DICT_WITHOIT_VALUES = {  
        WaterCheckerWithoutValues(False,False): ['ES0000'],
        WaterCheckerWithoutValues(False,True): ['EC0000','PR0111','PR1111'],
        WaterCheckerWithoutValues(True,False): ['EH0000','PR0111','PR1111'],
        WaterCheckerWithoutValues(True,True): ['EC0000','PR0111','PR1111'],
    }
    def __get_house_dict_index(self, people_num):
        '''
        возвращает индекс словаря в зависимости от количества людей,
        проживающих в доме
        '''
        if people_num < 3:
            return 0
        if people_num < 5:
            return 1
        if people_num < 8:
            return 2
        return 3
    
    def __get_country_dict_index(self, people_num):
        '''
        возвращает индекс в списке логики для дачного дома
        '''
        if people_num < 3:
            return 0
        return 1
    def __get_extra_country_equipment_id(selfm, people_num):
        '''
        возращает id доп оборудования для дачных домов
        '''
        if people_num < 3:
            return 'BB0110'
        return 'BB0120'

    def __get_final_offers_ids(self, logic_dict, water_hard, water_iron, water_mpc:dict, people_num=None, smell=False):
        for checker in logic_dict.keys():
            if checker.check(water_hard, water_iron, water_mpc, smell):
                print(str(checker)+'\n', logic_dict[checker])
                if logic_dict == self.HOUSE_BASE_LOGIC_DICT or logic_dict == self.HOUSE_BASE_LOGIC_DICT_WITHOUT_VALUES:
                    index = self.__get_house_dict_index(people_num)
                    return FinalOffer(
                        logic_dict[checker][index]['main_filters_components'], 
                        logic_dict[checker][index]['kitchen_filters'], 
                        logic_dict[checker][index]['fillers'], 
                        {'usually':['BB0023']})
                if logic_dict == self.COUNTRY_HOUSE_LOGIC_DICT or logic_dict == self.COUNTRY_HOUSE_LOGIC_DICT_WITHOUT_VALUES:
                    index = self.__get_country_dict_index(people_num)
                    print(checker)
                    return FinalOffer(
                        logic_dict[checker][index]['main_filters_components'], 
                        logic_dict[checker][index]['kitchen_filters'], 
                        logic_dict[checker][index]['fillers'],
                        {'usually':self.__get_extra_country_equipment_id(people_num)})
                return FinalOffer(
                    kitchen_filters=logic_dict[checker],
                    extra_equipments={'usually': ['PR0000','PR0001'],
                    'special': ['FD0000','SL0000']})
    
    def get_offers_ids(self, water_ferum, water_hard, name_form: str, extra_water_parametrs:dict,people_num=None, smell=False):
        form_name_logic_dict = {
            'flat_form': self.FLAT_LOGIC_DICT,
            'country_house_form': self.COUNTRY_HOUSE_LOGIC_DICT,
            'house_form': self.HOUSE_BASE_LOGIC_DICT}
        print('=='*20)
        print('smell:',smell)
        return self.__get_final_offers_ids(form_name_logic_dict[name_form], 
        water_hard=water_hard, 
        water_iron=water_ferum, 
        people_num=people_num,
        smell=smell,
        water_mpc=extra_water_parametrs)