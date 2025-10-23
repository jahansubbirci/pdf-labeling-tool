# ===== ui/label_panel.py =====

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from core.label_manager import LabelManager

class LabelPanel:
    '''Manages the label input and display panel'''
    
    def __init__(self, parent: ttk.Frame, label_manager: LabelManager):
        self.parent = parent
        self.label_manager = label_manager
        self.current_page = 0
        
        self.label_text_var = tk.StringVar(value='')
        self.listbox = None
        
        # Callbacks
        self.on_delete_selected: Optional[Callable] = None
        self.on_clear_page: Optional[Callable] = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        '''Setup the UI components'''
        ttk.Label(self.parent, text='Label Input', font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Label entry
        ttk.Label(self.parent, text='Label Text:').pack(anchor=tk.W, padx=5)
        ttk.Entry(self.parent, textvariable=self.label_text_var, width=30).pack(padx=5, pady=5)
        
        # Instructions
        ttk.Label(self.parent, text='Instructions:', font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=(10, 0))
        instructions = tk.Text(self.parent, height=5, wrap=tk.WORD, font=('Arial', 9))
        instructions.pack(padx=5, pady=5, fill=tk.X)
        instructions.insert('1.0', '1. Enter label text above\\n2. Click and drag on PDF to create labeled region\\n3. Labels are saved per page\\n4. Double-click labels in list to delete')
        instructions.config(state=tk.DISABLED)
        
        # Labels list
        ttk.Label(self.parent, text='Current Page Labels:', font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=5, pady=(10, 0))
        
        list_frame = ttk.Frame(self.parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        self.listbox.bind('<Double-Button-1>', lambda e: self._handle_delete())
        
        ttk.Button(self.parent, text='Delete Selected Label', command=self._handle_delete).pack(pady=5)
        ttk.Button(self.parent, text='Clear All Page Labels', command=self._handle_clear).pack(pady=5)
    
    def get_label_text(self) -> str:
        '''Get current label text'''
        return self.label_text_var.get().strip()
    
    def set_page(self, page_num: int):
        '''Set current page and update display'''
        self.current_page = page_num
        self.update_list()
    
    def update_list(self):
        '''Update the labels listbox'''
        self.listbox.delete(0, tk.END)
        labels = self.label_manager.get_labels(self.current_page)
        for i, label in enumerate(labels):
            self.listbox.insert(tk.END, f'{i+1}. {label.label_text} @ ({int(label.x)}, {int(label.y)})')
    
    def _handle_delete(self):
        '''Handle delete button click'''
        if self.on_delete_selected:
            self.on_delete_selected()
    
    def _handle_clear(self):
        '''Handle clear button click'''
        if self.on_clear_page:
            self.on_clear_page()

# ====================