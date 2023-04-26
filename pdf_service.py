import math
import time
import json
from io import BytesIO
from typing import List, Optional, Dict
from fitz import Document

class PdfService:
    

    @classmethod
    def split(cls, file_path: str, proc_size: int = 1) -> List[BytesIO]:
        pdf_buffers = []
        pdf = Document(file_path)
        page_size = pdf.page_count
        split_size = math.ceil(page_size/proc_size)

        for from_page in range(0, page_size + 1, split_size):
            if from_page == page_size:
                continue

            to_page = min(from_page + split_size, page_size + 1) - 1

            pdf_bytes = pdf.convert_to_pdf(from_page, to_page)
            new_doc = Document(stream=pdf_bytes, filetype='pdf')

            pdf_buffer = BytesIO()
            
            # File name that holds page numbers (e.g.:' 0_1_2_3.pdf')
            fn = '_'.join([str(i) for i in range(from_page, to_page+1)])

            new_doc.save(pdf_buffer)
            pdf_buffer.name = f'{fn}.pdf'
            pdf_buffers.append(pdf_buffer)

        if len(pdf_buffers) < proc_size:
            pdf_buffers.extend([None] * (proc_size - len(pdf_buffers)))

        return pdf_buffers

    @classmethod
    def extract(cls, pdf_buffer: BytesIO,
                    rank: int = 0,
                    procname: Optional[str] = None,
                    size: int = 0) -> Dict:
        if not pdf_buffer:
            return {}
        
        texts = {}
        msg = f"Text extraction by {procname}, rank {rank} out of {size-1} processors."
        print(f"{msg} >> {pdf_buffer.name}")

        """
        pdf_buffer.name = "0_1_2_3.pdf"
        page_idf = [0, 1, 2, 3]
        """
        page_idf = pdf_buffer.name.split('.')[:-1][0].split('_')
        pdf_doc = Document(stream=pdf_buffer.getvalue(), filetype='pdf')

        for no, page in enumerate(pdf_doc):
            texts[page_idf[no]] = []
            data = page.get_text('json')
            data = json.loads(data)

            lines = [line for block in data.get('blocks', []) for line in block.get('lines', [])]
            spans = [span for line in lines for span in line.get('spans', [])]

            """
            texts = [span.get('text').strip() for span in spans if text]
            """
            for span in spans:
                text = span.get('text').strip()
                if not text:
                    continue
            
                texts[page_idf[no]].append(text)

        time.sleep(5)
        return texts