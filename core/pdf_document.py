# ===== core/pdf_document.py =====

import fitz  # PyMuPDF
from PIL import Image
from typing import Optional

class PDFDocument:
    '''Handles PDF operations and rendering'''
    
    def __init__(self):
        self.document = None
        self.file_path = None
        self.total_pages = 0
        self.current_page = 0
        self.zoom_level = 1.0
    
    def open(self, file_path: str) -> bool:
        '''Open a PDF file'''
        try:
            self.document = fitz.open(file_path)
            self.file_path = file_path
            self.total_pages = len(self.document)
            self.current_page = 0
            return True
        except Exception as e:
            raise Exception(f'Failed to open PDF: {str(e)}')
    
    def close(self):
        '''Close the current PDF document'''
        if self.document:
            self.document.close()
            self.document = None
    
    def render_page(self, page_num: int) -> Optional[Image.Image]:
        '''Render a specific page as PIL Image'''
        if not self.document or page_num >= self.total_pages:
            return None
        
        page = self.document[page_num]
        mat = fitz.Matrix(self.zoom_level, self.zoom_level)
        pix = page.get_pixmap(matrix=mat)
        
        img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        return img
    
    def next_page(self) -> bool:
        '''Move to next page'''
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            return True
        return False
    
    def prev_page(self) -> bool:
        '''Move to previous page'''
        if self.current_page > 0:
            self.current_page -= 1
            return True
        return False
    
    def zoom_in(self):
        '''Increase zoom level'''
        self.zoom_level = min(self.zoom_level + 0.2, 3.0)
    
    def zoom_out(self):
        '''Decrease zoom level'''
        self.zoom_level = max(self.zoom_level - 0.2, 0.5)
    
    def get_page_info(self) -> str:
        '''Get current page information'''
        if self.document:
            return f'Page: {self.current_page + 1} / {self.total_pages}'
        return 'No PDF loaded'
