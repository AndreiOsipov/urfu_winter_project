import pandas as pd
import numpy as np

class ExcelEquipment:
    def __init__(self, equipment_id, name, barcode, price, equipment_type) -> None:
        self.id = str(equipment_id)
        self.name = str(name)
        self.barcode = str(barcode)
        self.price = float(price)
        self.type = str(equipment_type)
    
    def __str__(self) -> str:
        return str(self.id)

class ExcelParser:

    __equipment_list = []
    __equipment_type = ''

    def __add_equipments_from_rows(self, row): 
        if row[0] is np.nan and not row[1] is np.nan:
                self.__equipment_type = row[1]
        else:
            self.__equipment_list.append(
                ExcelEquipment(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    self.__equipment_type))

    def generate_equipment_list(self, uploaded_file) -> ExcelEquipment:
        for chunk in uploaded_file.chunks():
            xl = pd.ExcelFile(chunk)
            parsed_data = xl.parse(xl.sheet_names[0])
            parsed_data.apply(self.__add_equipments_from_rows, axis=1)
            return self.__equipment_list
