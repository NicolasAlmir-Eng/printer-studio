import tkinter as tk
from tkinter import ttk
import subprocess
from maintenance import run_head_cleaning, run_nozzle_check, check_ink_usb

def build_tools_tab(notebook, app):
    tab = ttk.Frame(notebook, style="Card.TFrame")
    notebook.add(tab, text="  🔧  Ferramentas  ")
    inner = ttk.Frame(tab, style="Card.TFrame")
    inner.pack(fill="both", expand=True, padx=20, pady=18)

    ttk.Label(inner, text="Gestão e Diagnóstico do Sistema", style="CyanSection.TLabel").pack(anchor="w", pady=(0, 15))

    f_sys = ttk.LabelFrame(inner, text=" Atalhos do Sistema Ubuntu ", padding=15, style="Card.TFrame")
    f_sys.pack(fill="x", pady=10)
    ttk.Label(f_sys, text="Use essas opções para adicionar impressoras Wi-Fi ou gerenciar a rede.", style="Muted.TLabel").pack(anchor="w", pady=(0,10))
    
    btn_frame1 = ttk.Frame(f_sys, style="Card.TFrame")
    btn_frame1.pack(fill="x")
    ttk.Button(btn_frame1, text="⚙️ Abrir Configurações Nativas (Ubuntu)", style="Secondary.TButton", command=lambda: subprocess.Popen(["system-config-printer"])).pack(side="left", padx=(0,10))
    ttk.Button(btn_frame1, text="🌐 Abrir Painel CUPS", style="Cyan.TButton", command=lambda: subprocess.Popen(["xdg-open", "http://localhost:631/printers/"])).pack(side="left")

    f_usb = ttk.LabelFrame(inner, text=" Manutenção via Cabo USB (escputil) ", padding=15, style="Card.TFrame")
    f_usb.pack(fill="x", pady=20)
    ttk.Label(f_usb, text="Essas opções funcionam melhor se a impressora estiver conectada via cabo USB.", style="Muted.TLabel").pack(anchor="w", pady=(0,10))
    
    btn_frame2 = ttk.Frame(f_usb, style="Card.TFrame")
    btn_frame2.pack(fill="x")
    ttk.Button(btn_frame2, text="💧 Executar Limpeza", style="Danger.TButton", command=lambda: run_head_cleaning(app)).pack(side="left", padx=(0,10))
    ttk.Button(btn_frame2, text="📄 Teste de Jatos (Nozzle)", style="Secondary.TButton", command=lambda: run_nozzle_check(app)).pack(side="left", padx=(0,10))
    ttk.Button(btn_frame2, text="Verificar Tinta (USB)", style="Secondary.TButton", command=lambda: check_ink_usb(app)).pack(side="left")
