from tkinter import ttk

class Colors:
    BG_ROOT   = "#F5F5F7"   # Cinza ultra claro (fundo da janela)
    BG_FRAME  = "#FFFFFF"   # Branco puro
    BG_INPUT  = "#E5E5EA"   # Cinza para caixas de texto/combobox
    BG_CARD   = "#FFFFFF"   # Fundo dos painéis
    BG_LOG    = "#1C1C1E"   # Terminal escuro estilo macOS
    FG_TEXT   = "#1D1D1F"   # Preto/Cinza escuro para texto
    FG_MUTED  = "#86868B"   # Texto secundário
    FG_WHITE  = "#FFFFFF"
    ACCENT    = "#007AFF"   # Azul Apple (Primário)
    ACCENT_2  = "#34C759"   # Verde Apple (Sucesso)
    ACCENT_DK = "#0056B3"   # Azul mais escuro (Hover)
    DANGER    = "#FF3B30"   # Vermelho Apple
    WARNING   = "#FF9500"   # Laranja Apple
    CYAN      = "#5AC8FA"   # Azul Ciano Apple

class LogLevel:
    INFO, OK, WARN, ERR, DEBUG = "INFO", "OK", "WARN", "ERR", "DBG"
    COLORS = {"INFO": "#5AC8FA", "OK": "#34C759", "WARN": "#FF9500", "ERR": "#FF3B30", "DBG": "#86868B"}

def setup_styles():
    style = ttk.Style()
    try: style.theme_use("clam")
    except: pass

    # Estilos Base
    style.configure(".", background=Colors.BG_ROOT, foreground=Colors.FG_TEXT, fieldbackground=Colors.BG_INPUT, borderwidth=0)
    style.configure("TFrame", background=Colors.BG_ROOT)
    style.configure("Card.TFrame", background=Colors.BG_CARD)
    
    # Textos e Títulos
    style.configure("TLabel", background=Colors.BG_ROOT, foreground=Colors.FG_TEXT, font=("Helvetica", 10))
    style.configure("Card.TLabel", background=Colors.BG_CARD, foreground=Colors.FG_TEXT)
    style.configure("Muted.TLabel", background=Colors.BG_CARD, foreground=Colors.FG_MUTED, font=("Helvetica", 9))
    style.configure("Title.TLabel", background=Colors.BG_ROOT, foreground=Colors.FG_TEXT, font=("Helvetica", 22, "bold"))
    style.configure("Subtitle.TLabel", background=Colors.BG_ROOT, foreground=Colors.FG_MUTED, font=("Helvetica", 10))
    style.configure("Section.TLabel", background=Colors.BG_CARD, foreground=Colors.ACCENT, font=("Helvetica", 12, "bold"))
    style.configure("CyanSection.TLabel", background=Colors.BG_CARD, foreground=Colors.ACCENT, font=("Helvetica", 12, "bold"))
    
    # Inputs
    style.configure("TEntry", fieldbackground=Colors.BG_INPUT, foreground=Colors.FG_TEXT, insertcolor=Colors.ACCENT, borderwidth=0, padding=8)
    style.configure("TCombobox", fieldbackground=Colors.BG_INPUT, foreground=Colors.FG_TEXT, background=Colors.BG_INPUT, arrowcolor=Colors.FG_TEXT, borderwidth=0, padding=6)
    style.map("TCombobox", fieldbackground=[("readonly", Colors.BG_INPUT)], foreground=[("readonly", Colors.FG_TEXT)])
    
    # Botões (Estilo Apple Flat)
    style.configure("Primary.TButton", background=Colors.ACCENT, foreground=Colors.BG_FRAME, font=("Helvetica", 10, "bold"), padding=(14, 8))
    style.map("Primary.TButton", background=[("active", Colors.ACCENT_DK), ("disabled", "#D1D1D6")])
    
    style.configure("Secondary.TButton", background=Colors.BG_INPUT, foreground=Colors.FG_TEXT, font=("Helvetica", 10), padding=(10, 6))
    style.map("Secondary.TButton", background=[("active", "#D1D1D6")])
    
    style.configure("Success.TButton", background=Colors.ACCENT_2, foreground=Colors.BG_FRAME, font=("Helvetica", 10, "bold"), padding=(14, 8))
    style.map("Success.TButton", background=[("active", "#28A745"), ("disabled", "#D1D1D6")])
    
    style.configure("Danger.TButton", background=Colors.DANGER, foreground=Colors.BG_FRAME, font=("Helvetica", 9, "bold"), padding=(10, 6))
    style.map("Danger.TButton", background=[("active", "#D70015")])
    
    style.configure("Cyan.TButton", background=Colors.BG_INPUT, foreground=Colors.ACCENT, font=("Helvetica", 10, "bold"), padding=(14, 8))
    style.map("Cyan.TButton", background=[("active", "#D1D1D6")])

    # Abas e Barras
    style.configure("TProgressbar", background=Colors.ACCENT, troughcolor=Colors.BG_INPUT, borderwidth=0, thickness=4)
    style.configure("TNotebook", background=Colors.BG_ROOT, borderwidth=0)
    style.configure("TNotebook.Tab", background=Colors.BG_INPUT, foreground=Colors.FG_MUTED, padding=(18, 10), font=("Helvetica", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", Colors.BG_CARD)], foreground=[("selected", Colors.ACCENT)])

    # Tabelas
    style.configure("Treeview", background=Colors.BG_ROOT, foreground=Colors.FG_TEXT, fieldbackground=Colors.BG_ROOT, borderwidth=0, rowheight=28)
    style.configure("Treeview.Heading", background=Colors.BG_INPUT, foreground=Colors.FG_TEXT, font=("Helvetica", 10, "bold"), borderwidth=0)
    style.map("Treeview", background=[("selected", Colors.ACCENT)], foreground=[("selected", Colors.BG_FRAME)])