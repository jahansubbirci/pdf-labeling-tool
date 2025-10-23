# ===== main.py =====

import tkinter as tk
from ui.main_window import PDFLabelingTool

def main():
    root = tk.Tk()
    app = PDFLabelingTool(root)
    app.run()

if __name__ == '__main__':
    main()
# ====================