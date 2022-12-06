class Filler:
    def __init__(self, filler_id, filler_v, filler_price) -> None:
        self.id = filler_id
        self.v = filler_v
        self.price = filler_price

class Combination:
    def __init__(self, ferum : tuple, hard: tuple) -> None:
        self.ferum_begin = ferum[0]
        self.ferum_end = ferum[1]
        self.hard_begin = hard[0]
        self.hart_end = hard[1]

class Logic:
    EM_25 = Filler('EM0001', 25, 5)
    EM_50 = Filler('EM0001', 50, 10)
    EM_60 = Filler('EM0001', 62.5, 13)
    EM_80 = Filler('EM0001', 80, 17)
    EMP_50 = Filler('EM0002', 50, 4)
    EMP_62 = Filler('EM0002', 62.5, 5)
    EMP_80 = Filler('EM0002', 80, 18)
    EMC_50 = Filler('EM0003', 50, 10)
    EMC_62 = Filler('EM0003', 62.5, 15)
    EMC_80 = Filler('EM0003', 80, 20)
    SM_25 = Filler('SM0000', 25, 15)
    SM_50 = Filler('SM0000', 50, 17)
    SM_62 = Filler('SM0000', 62.5, 20)
    SM_80 = Filler('SM0000', 80, 25)
    FM_50 = Filler('FM0000', 50, 20)
    FM_62 = Filler('FM0000', 62.5, 25)
    FM_80 = Filler('FM0000', 80, 30)
    SA_50 = Filler('SA0000', 50, 12)
    ABS_MAX = 100

    BASE_HOUSE_FERUM_HARD_COMBINES = [
    Combination((0, 3), (0, 0.3)), 
    Combination((0, 3), (0.3, 0.9)), 
    Combination((0, 3), (0.9, 8)),
    Combination((3, 8), (0, 0.3)),
    Combination((3, 8), (0.3, 8)),
    Combination((8, 15), (0, 0.3)),
    Combination((8, 15), (0.3, 8)),
    Combination((8, 15),(8, ABS_MAX)),
    Combination((15, ABS_MAX),(8, ABS_MAX))
    ]
    COUNTRY_HOUSE_FERUM_HARD_COMBINES = [
        Combination((0, 3), (0, 0.3)),
        Combination((0, 3), (0.3, 0.9)),
        Combination((3, 7), (0, 0.3)),
        Combination((3, 7), (0.3, 0.9)),
    ]
    FLAT_FERUM_HARD_COMBINES = [
        Combination((0, 3),(0, 0.6)),
        Combination((0, 3),(0.6, 0.9)),
        Combination((3, 7),(0, 0.6)),
        Combination((3, 7),(0.6, 0.9)),
        Combination((7, ABS_MAX),(0.6, 0.9)),
        Combination((3, 7),(0.9, ABS_MAX)),
        Combination((7, ABS_MAX),(0.9, ABS_MAX)),
    ]
    HOUSE_BASE_LOGIC_DICT = {
        
        BASE_HOUSE_FERUM_HARD_COMBINES[0]: [
            
                    #ВВ0020 - BB20 (Карбон-блок)
                    #ВВ0021 - BB20 (Феронить)
                    #ES0000 - Expert Standart 
                    #PR0111 - Профи Осмо
                    #WF0111 - Барьер Waterfort
                    #ЕC0000 - Expert Complex
                    #EX0000 - Expert смягчение
                    #KL1044 - Колонна 1044
                    #KL1252 - Колонна 1252
                    #KL1354 - Колонна 1354
                    #KL1465 - Колонна 1465
                    #BU0034 - Блок управления 100v3/4
                    #BU1001 - Блок управления 100V1 
                    #EM0025 - Ecomix A (25л)
                    #EM0050 - Ecomix A (50л)
                    #EM0060 - Ecomix A (62,5л)
                    #EM0800 - Ecomix A (80л)
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
                    #ВA0100 - Колонна аэрации Barier Aero Pro 100
                    #KG0050 - 50 кг соли
                    #SB0000 - Солевой бак       
                    {'main_filters_components': ['BB0020'], 'kitchen_filters': ['ES0000', 'PR0111', 'WF0111']},
                    {'main_filters_components': ['BB0020'], 'kitchen_filters': ['ES0000', 'PR0111', 'WF0111']},
                    {'main_filters_components': ['BB0020'], 'kitchen_filters': ['ES0000', 'PR0111', 'WF0111']},
                    {'main_filters_components': ['BB0020'], 'kitchen_filters': ['ES0000', 'PR0111', 'WF0111']}
                    ],
        BASE_HOUSE_FERUM_HARD_COMBINES[1]: [
                    {'main_filters_components': ['BB0021'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111']},
                    {'main_filters_components': ['KL1044', 'BU0034', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_25, SA_50]},
                    {'main_filters_components': ['KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_25, SA_50]},
                    {'main_filters_components': ['KL1465', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_80, SA_50]}
                    ],
        BASE_HOUSE_FERUM_HARD_COMBINES[2]: [
                    {'main_filters_components': ['KL1044', 'BU0034', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_25, SA_50]},
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_50, SA_50]},
                    {'main_filters_components': ['KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EMC_62, SA_50]},
                    {'main_filters_components': ['KL1465', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EMC_80, SA_50]}
                    ],
        BASE_HOUSE_FERUM_HARD_COMBINES[3]: [
                    {'main_filters_components': ['KL1044', 'BU0034', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers':[SM_25, SA_50]},
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers':[SM_50, SA_50]},
                    {'main_filters_components': ['KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers':[SM_62, SA_50]},
                    {'main_filters_components': ['KL1465', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers':[SM_80, SA_50]}
                    ],
        BASE_HOUSE_FERUM_HARD_COMBINES[4]: [
                    {'main_filters_components': ['KL1044', 'BU0034', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_25, SA_50]},
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000',  'PR0111', 'WF0111'], 'fillers':[EM_50, SA_50]},
                    {'main_filters_components': ['KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_60, SA_50]},
                    {'main_filters_components': ['KL1465', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers':[EM_80, SA_50]}
                    ],
        BASE_HOUSE_FERUM_HARD_COMBINES[5]: [
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers': [SM_50, SA_50]},
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EX0000', 'PR0111', 'WF0111'], 'fillers': [SM_50, SA_50]},
                    {'main_filters_components': [''], 'kitchen_filters': ['']},
                    {'main_filters_components': [''], 'kitchen_filters': ['']}
                    ],
        BASE_HOUSE_FERUM_HARD_COMBINES[6]: [
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers': [EM_50, SA_50]},
                    {'main_filters_components': ['KL1252', 'BU1001', 'SB0000', 'BB0020', 'KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': ['EC0000', 'PR0111', 'WF0111'], 'fillers': [EMC_50, SA_50, EM_60, SA_50]},
                    {'main_filters_components': ['KL1354', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': [''], 'fillers': [EM_50, SA_50, EM_60, SA_50]},
                    {'main_filters_components': ['KL1465', 'BU1001', 'SB0000', 'BB0020'], 'kitchen_filters': [''], 'fillers': [EM_50, SA_50, EM_80, SA_50]}
                    ],
        BASE_HOUSE_FERUM_HARD_COMBINES[7]: [
                    {'main_filters_components': ['ВA0100', 'KL1252', 'FM0050', 'KL1252', 'SB0000', 'BB0020'], 'kitchen_filters': [''], 'fillers': [EMP_50, SA_50]},
                    {'main_filters_components': ['ВA0100', 'KL1354', 'FM0062', 'KL1354', 'SB0000', 'BB0020'], 'kitchen_filters': [''], 'fillers': [EMP_62, SA_50]},
                    {'main_filters_components': ['ВA0100', 'KL1354', 'FM0062', 'KL1354', 'SB0000', 'BB0020'], 'kitchen_filters': [''], 'fillers': [EMP_62, SA_50]},
                    {'main_filters_components': ['ВA0100', 'KL1465', 'FM0080', 'KL1465', 'SB0000', 'BB0020'], 'kitchen_filters': [''], 'fillers': [EM_80, SA_50]}
                    ],
        BASE_HOUSE_FERUM_HARD_COMBINES[8]: [
                    {'main_filters_components': ['ВA0100', 'KL1252', 'FM0050', 'KL1252', 'SB0000', 'BB0020'], 'kitchen_filters': [''], 'fillers': [EMC_50, SA_50]},
                    {'main_filters_components': ['ВA0100', 'KL1354', 'FM0062', 'KL1354', 'SB0000', 'BB0020'], 'kitchen_filters': [''], 'fillers': [EMP_62, SA_50]},
                    {'main_filters_components': ['ВA0100', 'KL1354', 'FM0062', 'KL1354', 'SB0000', 'BB0020'], 'kitchen_filters': [''], 'fillers': [EMP_62, SA_50]},
                    {'main_filters_components': ['ВA0100', 'KL1465', 'FM0080', 'KL1465', 'SB0000', 'BB0020'], 'kitchen_filters': [''], 'fillers': [EM_80, SA_50]}
                    ],
    }
    #BB0010 -- bb10 карбон-блок
    #PR1111 -- m
    #BB0011 -- bb10 ферронить
    #BB0022 -- bb20 смягчение
    #EX0000 -- expert hard
    COUNTRY_HOUSE_LOGIC_DICT = {
        COUNTRY_HOUSE_FERUM_HARD_COMBINES[0] : [
            {'main_filters_components': ['BB0010'], 'kitchen_filters': ['ES0000', 'PR0111', 'PR1111']},
            {'main_filters_components': ['BB0020'], 'kitchen_filters': ['ES0000', 'PR0111', 'PR1111']}
        ],
        COUNTRY_HOUSE_FERUM_HARD_COMBINES[1] : [
            {'main_filters_components': ['BB0010'], 'kitchen_filters': ['EC0000', 'PR0111', 'PR1111']},
            {'main_filters_components': ['BB0021'], 'kitchen_filters': ['EC0000', 'PR0111', 'PR1111']}],
        COUNTRY_HOUSE_FERUM_HARD_COMBINES[2] : [
            {'main_filters_components': ['BB0022'], 'kitchen_filters': ['ES0000', 'PR0111', 'PR1111']},
            {'main_filters_components': ['BB0022'], 'kitchen_filters': ['ES0000', 'PR0111', 'PR1111']}
            ],
        COUNTRY_HOUSE_FERUM_HARD_COMBINES[3] : [
            {'main_filters_components': ['BB0011', 'BB0022'], 'kitchen_filters': ['EC0000', 'PR0111', 'PR1111']},
            {'main_filters_components': ['BB0021', 'BB0022'], 'kitchen_filters': ['EC0000', 'PR0111', 'PR1111']}
            ],
    }
    FLAT_LOGIC_DICT = {
        FLAT_FERUM_HARD_COMBINES[0]: {'kitchen_filters':['ES0000']},
        FLAT_FERUM_HARD_COMBINES[0]: {'kitchen_filters':['EC0000', 'PR0111', 'PR1111']},
        FLAT_FERUM_HARD_COMBINES[0]: {'kitchen_filters':['EH0000', 'PR0111', 'PR1111']},
        FLAT_FERUM_HARD_COMBINES[0]: {'kitchen_filters':['EC0000', 'PR0111', 'PR1111']},
        FLAT_FERUM_HARD_COMBINES[0]: {'kitchen_filters':['PR0111', 'PR1111']},
        FLAT_FERUM_HARD_COMBINES[0]: {'kitchen_filters':['PR0111', 'PR1111']},
        FLAT_FERUM_HARD_COMBINES[0]: {'kitchen_filters':['PR0111', 'PR1111']},
    }
    def __get_dict_index(self, people_num):
        
        if people_num < 3:
            return 0
        if people_num < 5:
            return 1
        if people_num < 8:
            return 2
        return 3

    def get_id_lists(self, water_ferum, water_hard, people_num, name_form: str):
        #отрефакторить
        build_logic_dict = {
            'flat_form':{'combines': self.FLAT_FERUM_HARD_COMBINES, 'equipment': self.FLAT_LOGIC_DICT},
            'country_form':{'combines': self.COUNTRY_HOUSE_FERUM_HARD_COMBINES, 'equipment': self.COUNTRY_HOUSE_LOGIC_DICT},
            'house_form':{'combines': self.BASE_HOUSE_FERUM_HARD_COMBINES, 'equipment': self.HOUSE_BASE_LOGIC_DICT},
        }
        for comb in build_logic_dict[name_form]['combines']:
            if (water_ferum >= comb.ferum_begin and water_ferum <= comb.ferum_end) \
                and (water_hard >= comb.hard_begin and water_ferum < comb.hart_end):
                
                return build_logic_dict[name_form]['equipment'][comb][self.__get_dict_index(people_num)]