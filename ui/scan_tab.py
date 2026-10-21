import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from theme import Colors
from scanner import start_scan_job, start_multi_scan_job
from maintenance import discover_scanners

def build_scan_tab(notebook, app):
    tab = ttk.Frame(notebook, style="Card.TFrame")
    notebook.add(tab, text="  📷  Scanner  ")
    inner = ttk.Frame(tab, style="Card.TFrame")
    inner.pack(fill="both", expand=True, padx=20, pady=18)

    ttk.Label(inner, text="Digitalização Assistida", style="Section.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))

    ttk.Label(inner, text="Dispositivo:", style="Card.TLabel").grid(row=1, column=0, sticky="e", pady=6, padx=(0, 8))
    app.var_device = tk.StringVar(value=app.config.scanner_device)
    ttk.Entry(inner, textvariable=app.var_device, width=50).grid(row=1, column=1, sticky="ew", pady=6)
    ttk.Button(inner, text="🔍 Descobrir", style="Secondary.TButton", command=lambda: discover_scanners(app, app.var_device)).grid(row=1, column=2, padx=(8, 0))

    ttk.Label(inner, text="Resolução:", style="Card.TLabel").grid(row=2, column=0, sticky="e", pady=6, padx=(0, 8))
    app.var_dpi = tk.StringVar(value=app.config.dpi)
    ttk.Combobox(inner, textvariable=app.var_dpi, state="readonly", width=16, values=["150", "200", "300", "600", "1200", "4800"]).grid(row=2, column=1, sticky="w", pady=6)

    ttk.Label(inner, text="Modo de Cor:", style="Card.TLabel").grid(row=3, column=0, sticky="e", pady=6, padx=(0, 8))
    app.var_color = tk.StringVar(value=app.config.color_mode)
    ttk.Combobox(inner, textvariable=app.var_color, state="readonly", width=16, values=["Color", "Gray", "Lineart"]).grid(row=3, column=1, sticky="w", pady=6)

    opts = ttk.Frame(inner, style="Card.TFrame")
    opts.grid(row=4, column=0, columnspan=3, sticky="w", pady=(15, 10))
    
    app.var_ocr = tk.BooleanVar(value=app.config.ocr_enabled)
    app.var_trim = tk.BooleanVar(value=app.config.auto_trim)
    app.var_open = tk.BooleanVar(value=app.config.auto_open_after_scan)

    tk.Checkbutton(opts, text="Extrair Texto (OCR)", variable=app.var_ocr, bg=Colors.BG_CARD, fg=Colors.CYAN, selectcolor=Colors.BG_INPUT, activebackground=Colors.BG_CARD, activeforeground=Colors.CYAN, font=("Helvetica", 9, "bold"), borderwidth=0).pack(side="left", padx=(0, 20))
    tk.Checkbutton(opts, text="Remover Bordas", variable=app.var_trim, bg=Colors.BG_CARD, fg=Colors.FG_TEXT, selectcolor=Colors.BG_INPUT, activebackground=Colors.BG_CARD, font=("Helvetica", 9), borderwidth=0).pack(side="left", padx=(0, 20))
    tk.Checkbutton(opts, text="Abrir após concluir", variable=app.var_open, bg=Colors.BG_CARD, fg=Colors.FG_TEXT, selectcolor=Colors.BG_INPUT, activebackground=Colors.BG_CARD, font=("Helvetica", 9), borderwidth=0).pack(side="left", padx=(0, 20))

    ttk.Label(inner, text="Salvar em:", style="Card.TLabel").grid(row=5, column=0, sticky="e", pady=6, padx=(0, 8))
    app.var_savedir = tk.StringVar(value=app.config.save_dir)
    ttk.Entry(inner, textvariable=app.var_savedir, width=50).grid(row=5, column=1, sticky="ew", pady=6)
    ttk.Button(inner, text="📁", style="Secondary.TButton", command=lambda: _choose_dir(app.var_savedir)).grid(row=5, column=2, padx=(8, 0))

    def _choose_dir(var):
        d = filedialog.askdirectory()
        if d: var.set(d)

    def on_scan():
        if app.busy: return
        Path(app.var_savedir.get()).mkdir(parents=True, exist_ok=True)
        path = filedialog.asksaveasfilename(defaultextension=".png", initialdir=app.var_savedir.get(), initialfile="scan.png")
        if path: start_scan_job(app, path, app.var_device.get(), app.var_color.get(), app.var_dpi.get(), app.var_trim.get(), app.var_ocr.get(), app.var_open.get())

    def on_scan_multi():
        if app.busy: return
        out = filedialog.asksaveasfilename(defaultextension=".pdf", initialdir=app.var_savedir.get(), initialfile="multi_scan.pdf")
        if out: start_multi_scan_job(app, out, app.var_savedir.get(), app.var_device.get(), app.var_color.get(), app.var_dpi.get(), app.var_trim.get(), app.var_ocr.get())

    actions = ttk.Frame(inner, style="Card.TFrame")
    actions.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(25, 0))
    ttk.Button(actions, text="📥 Digitalizar", style="Success.TButton", command=on_scan).pack(side="left")
    ttk.Button(actions, text="🗂 Múltiplas Páginas", style="Primary.TButton", command=on_scan_multi).pack(side="left", padx=8)

    app.progress_scan = ttk.Progressbar(inner, mode="indeterminate")
    app.progress_scan.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(16, 0))
    inner.columnconfigure(1, weight=1)
