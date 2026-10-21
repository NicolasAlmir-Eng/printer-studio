#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import queue
from datetime import datetime

from config import AppConfig, ProfileManager, HistoryManager
from theme import Colors, LogLevel, setup_styles
from maintenance import check_dependencies
from ui.scan_tab import build_scan_tab
from ui.print_tab import build_print_tab
from ui.tools_tab import build_tools_tab

class PrinterStudioPro:
    def __init__(self, root):
        self.root = root
        self.config = AppConfig.load()
        self.profiles = ProfileManager()
        self.history = HistoryManager()
        self.log_queue = queue.Queue()
        self.busy = False

        self.root.title("Printer Studio")
        self.root.geometry("950x920")
        self.root.minsize(850, 800)
        self.root.configure(bg=Colors.BG_ROOT)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self.root.update_idletasks()
        w, h = 950, 920
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        setup_styles()
        self._build_ui()
        self._start_log_pump()
        check_dependencies(self.log)

        self.log("Printer Studio (macOS Edition) iniciado.", LogLevel.OK)

    def log(self, msg: str, level: str = LogLevel.INFO):
        self.log_queue.put((level, msg, datetime.now().strftime("%H:%M:%S")))

    def _build_ui(self):
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=20, pady=(24, 16))

        # Cabeçalho limpo estilo Mac
        ttk.Label(header, text="Printer Studio", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Scanner c/ OCR · Impressora HD · Manutenção", style="Subtitle.TLabel").pack(anchor="w", pady=(2, 0))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Tabs
        build_scan_tab(self.notebook, self)
        build_print_tab(self.notebook, self)
        build_tools_tab(self.notebook, self)
        self._build_log_tab()
        self._build_statusbar()

    def _build_log_tab(self):
        tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(tab, text="  Logs de Atividade  ")
        self.txt_log = tk.Text(tab, bg=Colors.BG_LOG, fg=Colors.FG_WHITE, font=("Menlo", 10), state="disabled", borderwidth=0, highlightthickness=0)
        self.txt_log.pack(fill="both", expand=True, padx=15, pady=15)
        for lvl, color in LogLevel.COLORS.items(): 
            self.txt_log.tag_configure(lvl, foreground=color)

    def _build_statusbar(self):
        self.lbl_status = tk.Label(self.root, text="  Pronto", bg=Colors.BG_ROOT, fg=Colors.FG_MUTED, font=("Helvetica", 10), anchor="w")
        self.lbl_status.pack(fill="x", side="bottom", padx=20, pady=10)

    def _start_log_pump(self):
        def pump():
            try:
                while True:
                    level, msg, ts = self.log_queue.get_nowait()
                    self.txt_log.config(state="normal")
                    self.txt_log.insert("end", f"[{ts}] {msg}\n", level)
                    self.txt_log.config(state="disabled")
                    self.txt_log.see("end")
            except queue.Empty: pass
            self.root.after(100, pump)
        pump()

    def set_busy(self, on: bool):
        self.busy = on
        if hasattr(self, 'progress_scan'):
            if on: self.progress_scan.start(12)
            else: self.progress_scan.stop()

    def _on_close(self):
        self.config.save()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PrinterStudioPro(root)
    root.mainloop()