import docx
import io
from docx.document import Document


class DocxGenerator:
    def __init__(self) -> None:
        pass

    def generate_contract(self, complect_info, build_obkject_info, full_water_analisys=None):
        doc:Document = docx.Document()
        doc.add_heading('ПРОЕКТНАЯ СМЕТА', 0)
        doc.add_paragraph('Комплексной системы очистки воды')

        
        stream = io.BytesIO()
        
        doc.save(stream)
        print(stream)
        stream.seek(0)
        return stream