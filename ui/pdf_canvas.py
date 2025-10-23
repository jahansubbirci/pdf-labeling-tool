# ===== ui/pdf_canvas.py =====

import tkinter as tk
from PIL import Image, ImageTk
from typing import Tuple, List, Callable, Optional
from core.label_manager import LabelManager
from models.label import Label

class PDFCanvas:
    '''Handles PDF display and drawing interactions'''
    
    def __init__(self, canvas: tk.Canvas, label_manager: LabelManager):
        self.canvas = canvas
        self.label_manager = label_manager
        self.current_image = None
        self.current_page = 0
        
        # Drawing state
        self.rect_start = None
        self.drawing_rect = None
        
        # Callback
        self.on_rectangle_drawn: Optional[Callable] = None
        
        # Bind events
        self.canvas.bind('<ButtonPress-1>', self._on_mouse_down)
        self.canvas.bind('<B1-Motion>', self._on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_mouse_up)
    
    def display_image(self, img: Image.Image, page_num: int):
        '''Display an image on the canvas'''
        self.current_page = page_num
        self.current_image = ImageTk.PhotoImage(img)
        
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        
        self._draw_labels()
    
    def _draw_labels(self):
        '''Draw all labels for current page'''
        labels = self.label_manager.get_labels(self.current_page)
        for i, label in enumerate(labels):
            bbox = label.bbox
            self.canvas.create_rectangle(
                bbox[0], bbox[1], bbox[2], bbox[3],
                outline='red', width=2, tags=f'label_{i}'
            )
            self.canvas.create_text(
                bbox[0], bbox[1] - 5,
                text=label.label_text,
                anchor=tk.SW,
                fill='red',
                font=('Arial', 10, 'bold'),
                tags=f'label_{i}'
            )
    
    def _on_mouse_down(self, event):
        '''Handle mouse button press'''
        self.rect_start = (event.x, event.y)
    
    def _on_mouse_drag(self, event):
        '''Handle mouse drag'''
        if self.rect_start:
            if self.drawing_rect:
                self.canvas.delete(self.drawing_rect)
            
            x1, y1 = self.rect_start
            self.drawing_rect = self.canvas.create_rectangle(
                x1, y1, event.x, event.y,
                outline='blue', width=2, dash=(5, 5)
            )
    
    def _on_mouse_up(self, event):
        '''Handle mouse button release'''
        if self.rect_start and self.drawing_rect:
            x1, y1 = self.rect_start
            x2, y2 = event.x, event.y
            
            # Normalize coordinates
            bbox = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            
            # Only create label if rectangle is large enough
            if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:
                if self.on_rectangle_drawn:
                    self.on_rectangle_drawn(bbox)
            
            self.canvas.delete(self.drawing_rect)
            self.drawing_rect = None
            self.rect_start = None
    
    def refresh(self):
        '''Refresh the canvas to show updated labels'''
        # Remove old labels
        for item in self.canvas.find_all():
            tags = self.canvas.gettags(item)
            if any(tag.startswith('label_') for tag in tags):
                self.canvas.delete(item)
        
        self._draw_labels()

# ====================