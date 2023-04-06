import openpyxl
from openpyxl.styles import PatternFill
from openpyxl.worksheet.worksheet import Worksheet
from io import BytesIO

class ExcelEquipment:
    def __init__(self, equipment_id, name, barcode, price, equipment_type) -> None:
        self.id = str(equipment_id)
        self.name = str(name)
        self.barcode = str(barcode)
        self.price = float(price)
        self.type = str(equipment_type)
    
    def __str__(self) -> str:
        return str(self.id)

class ParsedEquipmentsFile:
    def __init__(self, uploaded_file, equipment_list, not_full_rows_indexes) -> None:
        self.file = uploaded_file
        self.equipment_list = equipment_list
        self.not_full_rows_indexes = not_full_rows_indexes

class ExcelParser:

    def is_equioment_type(self, row):
        return (row[0].value is None) and (row[2].value is None) and (row[3].value is None) and not (row[1].value is None)
    
    def is_null_row(self, row):
        return (row[0].value is None) and (row[1].value is None) and (row[2].value is None) and (row[3].value is None)
    
    def keys_cell_not_is_nan(self, row):
        return not((row[0].value is None) or (row[1].value is None) or (row[3].value is None))
    
    def get_parsed_excel(self, uploaded_file) -> ParsedEquipmentsFile:
        equipment_list = []
        not_full_rows = []
        current_equipment_type = ''
        for chunk in uploaded_file.chunks():
            wb :openpyxl.Workbook = openpyxl.load_workbook(BytesIO(chunk))
            sheet_names = wb.get_sheet_names()
            sheet:Worksheet = wb.get_sheet_by_name(sheet_names[0])
            rows = sheet.rows
            rows.__next__()
            for row in rows:
                if self.is_equioment_type(row):
                    current_equipment_type = row[1].value
                else:
                    if not self.is_null_row(row):
                        if self.keys_cell_not_is_nan(row):
                            equipment_list.append(ExcelEquipment(row[0].value,row[1].value,row[2].value,row[3].value,current_equipment_type))
                        else:
                            not_full_rows.append(row)
        wb.close()
        return ParsedEquipmentsFile(uploaded_file,equipment_list, not_full_rows)
