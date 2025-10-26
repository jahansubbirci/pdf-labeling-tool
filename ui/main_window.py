# ===== ui/main_window.py =====

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Tuple
from core.pdf_document import PDFDocument
from core.label_manager import LabelManager
from models.label import Label
from ui.pdf_canvas import PDFCanvas
from ui.label_panel import LabelPanel

class PDFLabelingTool:
    '''Main application class'''
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('PDF Labeling Tool')
        self.root.geometry('1200x800')
        
        # Initialize components
        self.pdf_doc = PDFDocument()
        self.label_manager = LabelManager()
        
        # UI components (will be initialized in setup)
        self.pdf_canvas = None
        self.label_panel = None
        self.page_label = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        '''Setup the main UI'''
        # Menu bar
        self._create_menu()
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - PDF viewer
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(left_frame, bg='gray')
        canvas.pack(fill=tk.BOTH, expand=True)
        
        self.pdf_canvas = PDFCanvas(canvas, self.label_manager)
        self.pdf_canvas.on_rectangle_drawn = self._on_rectangle_drawn
        
        # Navigation frame
        nav_frame = ttk.Frame(left_frame)
        nav_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(nav_frame, text='◀ Previous', command=self._prev_page).pack(side=tk.LEFT, padx=5)
        self.page_label = ttk.Label(nav_frame, text='Page: 0 / 0')
        self.page_label.pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text='Next ▶', command=self._next_page).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(nav_frame, text='Zoom:').pack(side=tk.LEFT, padx=(20, 5))
        ttk.Button(nav_frame, text='-', command=self._zoom_out, width=3).pack(side=tk.LEFT)
        ttk.Button(nav_frame, text='+', command=self._zoom_in, width=3).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Labels
        right_frame = ttk.Frame(main_frame, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_frame.pack_propagate(False)
        
        self.label_panel = LabelPanel(right_frame, self.label_manager)
        self.label_panel.on_delete_selected = self._delete_selected_label
        self.label_panel.on_clear_page = self._clear_page_labels
    
    def _create_menu(self):
        '''Create menu bar'''
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open PDF', command=self._open_pdf)
        file_menu.add_command(label='Save Labels', command=self._save_labels)
        file_menu.add_command(label='Load Labels', command=self._load_labels)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.quit)
    
    def _open_pdf(self):
        '''Open PDF file'''
        file_path = filedialog.askopenfilename(
            title='Select PDF file',
            filetypes=[('PDF files', '*.pdf'), ('All files', '*.*')]
        )
        
        if file_path:
            try:
                self.pdf_doc.open(file_path)
                self.label_manager.clear_all()
                self._display_current_page()
            except Exception as e:
                messagebox.showerror('Error', str(e))
    
    def _display_current_page(self):
        '''Display current page'''
        img = self.pdf_doc.render_page(self.pdf_doc.current_page)
        if img:
            self.pdf_canvas.display_image(img, self.pdf_doc.current_page)
            self.label_panel.set_page(self.pdf_doc.current_page)
            self.page_label.config(text=self.pdf_doc.get_page_info())
    
    def _next_page(self):
        '''Go to next page'''
        if self.pdf_doc.next_page():
            self._display_current_page()
    
    def _prev_page(self):
        '''Go to previous page'''
        if self.pdf_doc.prev_page():
            self._display_current_page()
    
    def _zoom_in(self):
        '''Zoom in'''
        self.pdf_doc.zoom_in()
        self._display_current_page()
    
    def _zoom_out(self):
        '''Zoom out'''
        self.pdf_doc.zoom_out()
        self._display_current_page()
    
    def _on_rectangle_drawn(self, bbox: Tuple[float, float, float, float]):
        '''Handle rectangle drawn on canvas'''
        label_text = self.label_panel.get_label_text()
        
        if not label_text:
            messagebox.showwarning('No Label', 'Please enter label text before drawing.')
            return
        
        # Create label
        x, y = bbox[0], bbox[1]
        label = Label(x, y, label_text, bbox)
        self.label_manager.add_label(self.pdf_doc.current_page, label)
        
        # Refresh display
        self.pdf_canvas.refresh()
        self.label_panel.update_list()
    
    def _delete_selected_label(self):
        '''Delete selected label from list'''
        selection = self.label_panel.listbox.curselection()
        if selection:
            index = selection[0]
            self.label_manager.delete_label(self.pdf_doc.current_page, index)
            self.pdf_canvas.refresh()
            self.label_panel.update_list()
    
    def _clear_page_labels(self):
        '''Clear all labels from current page'''
        if messagebox.askyesno('Confirm', 'Clear all labels from this page?'):
            self.label_manager.clear_page(self.pdf_doc.current_page)
            self.pdf_canvas.refresh()
            self.label_panel.update_list()
    
    def _save_labels(self):
        '''Save labels to file'''
        if not self.pdf_doc.file_path:
            messagebox.showwarning('No PDF', 'Please open a PDF first.')
            return
        
        file_path = filedialog.asksaveasfilename(
            title='Save Labels',
            defaultextension='.json',
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
        )
        
        if file_path:
            try:
                self.label_manager.save_to_file(file_path)
                messagebox.showinfo('Success', 'Labels saved successfully!')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to save labels: {str(e)}')
    
    def _load_labels(self):
        '''Load labels from file'''
        file_path = filedialog.askopenfilename(
            title='Load Labels',
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
        )
        
        if file_path:
            try:
                self.label_manager.load_from_file(file_path)
                self._display_current_page()
                messagebox.showinfo('Success', 'Labels loaded successfully!')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to load labels: {str(e)}')
    
    def run(self):
        '''Start the application'''
        self.root.mainloop()

# ====================