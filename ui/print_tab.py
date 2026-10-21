import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
import os
from theme import Colors
from printer import load_printers, run_print, process_and_print_image, cancel_all_jobs, get_queue, resume_printer

def build_print_tab(notebook, app):
    tab = ttk.Frame(notebook, style="Card.TFrame")
    notebook.add(tab, text="  🖨  Impressora  ")
    inner = ttk.Frame(tab, style="Card.TFrame")
    inner.pack(fill="both", expand=True, padx=20, pady=18)

    app.var_printer = tk.StringVar(value=app.config.last_printer)
    
    def refresh_printers():
        printers = load_printers()
        app.cb_printer["values"] = printers
        if printers and not app.var_printer.get(): app.var_printer.set(printers[0])

    ttk.Label(inner, text="Impressora:", style="Card.TLabel").grid(row=1, column=0, sticky="e", pady=6, padx=(0, 8))
    app.cb_printer = ttk.Combobox(inner, textvariable=app.var_printer, state="readonly", width=44)
    app.cb_printer.grid(row=1, column=1, columnspan=2, sticky="ew", pady=6)
    ttk.Button(inner, text="🔄", style="Secondary.TButton", command=refresh_printers).grid(row=1, column=3, padx=(8, 0))

    ttk.Label(inner, text="Tam. Papel:", style="Card.TLabel").grid(row=2, column=0, sticky="e", pady=6, padx=(0, 8))
    app.var_paper = tk.StringVar(value=app.config.paper_size)
    ttk.Combobox(inner, textvariable=app.var_paper, state="readonly", width=18, values=["A4", "A5", "Letter", "Legal", "Photo 10x15", "Photo 13x18"]).grid(row=2, column=1, sticky="w", pady=6)

    ttk.Label(inner, text="Tipo de Papel:", style="Card.TLabel").grid(row=2, column=2, sticky="e", pady=6, padx=(8, 0))
    app.var_paper_type = tk.StringVar(value=app.config.paper_type)
    ttk.Combobox(inner, textvariable=app.var_paper_type, state="readonly", width=16, values=["Plain", "Glossy", "Matte", "Envelope"]).grid(row=2, column=3, sticky="w", pady=6)

    ttk.Label(inner, text="Qualidade:", style="Card.TLabel").grid(row=4, column=0, sticky="e", pady=6, padx=(0, 8))
    app.var_quality = tk.StringVar(value=app.config.print_quality)
    ttk.Combobox(inner, textvariable=app.var_quality, state="readonly", width=18, values=["Draft", "Normal", "High", "Ultra"]).grid(row=4, column=1, sticky="w", pady=6)

    ttk.Label(inner, text="Modo de Cor:", style="Card.TLabel").grid(row=5, column=0, sticky="e", pady=6, padx=(0, 8))
    app.var_print_color = tk.StringVar(value=app.config.color_print_mode)
    ttk.Combobox(inner, textvariable=app.var_print_color, state="readonly", width=18, values=["Color", "Grayscale", "Black"]).grid(row=5, column=1, sticky="w", pady=6)

    ttk.Label(inner, text="Cópias:", style="Card.TLabel").grid(row=5, column=2, sticky="e", pady=6, padx=(8, 0))
    app.var_copies = tk.StringVar(value="1")
    ttk.Spinbox(inner, from_=1, to=999, textvariable=app.var_copies, width=6).grid(row=5, column=3, sticky="w", pady=6)

    chk_row = ttk.Frame(inner, style="Card.TFrame")
    chk_row.grid(row=9, column=0, columnspan=4, sticky="w", pady=(12, 4))
    app.var_duplex_p = tk.BooleanVar(value=False)
    app.var_borderless = tk.BooleanVar(value=app.config.borderless)

    for txt, var in [("Frente e verso", app.var_duplex_p), ("Sem bordas", app.var_borderless)]:
        tk.Checkbutton(chk_row, text=txt, variable=var, bg=Colors.BG_CARD, fg=Colors.FG_TEXT, selectcolor=Colors.BG_INPUT, activebackground=Colors.BG_CARD, activeforeground=Colors.ACCENT_2, font=("Helvetica", 9), borderwidth=0).pack(side="left", padx=(0, 16))

    def update_queue():
        for item in app.tree_jobs.get_children(): app.tree_jobs.delete(item)
        for job in get_queue(app.var_printer.get()): app.tree_jobs.insert("", "end", values=job)

    def _get_print_kwargs():
        return {
            "printer": app.var_printer.get(),
            "paper_size": app.var_paper.get(),
            "paper_type": app.var_paper_type.get(),
            "qual": app.var_quality.get(),
            "color_mode": app.var_print_color.get(),
            "copies": app.var_copies.get(),
            "landscape": False,
            "borderless": app.var_borderless.get(),
            "duplex": app.var_duplex_p.get(),
        }


    def _show_printing_animation(path, total_seconds, job_id, printer_name):
        try:
            from PIL import Image, ImageTk, ImageDraw
        except ImportError:
            return

        anim_win = tk.Toplevel(app.root)
        anim_win.title("Impressão Ativa")
        anim_win.geometry("450x580")
        anim_win.configure(bg=Colors.BG_ROOT)
        anim_win.attributes("-topmost", True)
        
        anim_win.update_idletasks()
        x = (anim_win.winfo_screenwidth() - 450) // 2
        y = (anim_win.winfo_screenheight() - 580) // 2
        anim_win.geometry(f"+{x}+{y}")

        lbl_status = ttk.Label(anim_win, text="Preparando...", style="Title.TLabel", font=("Helvetica", 16, "bold"))
        lbl_status.pack(pady=(25, 5))

        lbl_time = ttk.Label(anim_win, text=f"Documento #{job_id}", style="Subtitle.TLabel")
        lbl_time.pack(pady=(0, 15))

        c_width, c_height = 300, 350
        canvas = tk.Canvas(anim_win, width=c_width, height=c_height, bg=Colors.BG_ROOT, highlightthickness=0)
        canvas.pack()

        if path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            img = Image.open(path)
            img.thumbnail((c_width - 80, c_height - 100))
        else:
            img = Image.new('RGB', (160, 220), color='white')
            draw = ImageDraw.Draw(img)
            for i in range(10): draw.line((20, 30 + i*16, 140, 30 + i*16), fill="#E5E5EA", width=4)
                
        photo = ImageTk.PhotoImage(img)
        img_w, img_h = img.size

        start_y = 60 - img_h
        end_y = 70
        x_center = c_width // 2
        
        paper_id = canvas.create_rectangle(x_center - img_w//2, start_y, x_center + img_w//2, start_y + img_h, fill="#FFFFFF", outline="#D1D1D6", width=1)
        img_id = canvas.create_image(x_center, start_y, anchor="n", image=photo)
        canvas.image = photo 
        
        canvas.create_rectangle(0, 0, c_width, 60, fill=Colors.BG_ROOT, outline=Colors.BG_ROOT)
        canvas.create_line(20, 58, c_width-20, 58, width=14, fill="#E5E5EA", capstyle="round") 
        canvas.create_line(35, 60, c_width-35, 60, width=4, fill="#1C1C1E", capstyle="round")

        prog = ttk.Progressbar(anim_win, mode="determinate", maximum=100)
        prog.pack(fill="x", padx=50, pady=20)

        fps = 30
        total_frames = total_seconds * fps if total_seconds > 0 else 30
        y_step = (end_y - start_y) / total_frames

        job_status = {"state": "waiting"} 

        def poll_job_status():
            """Checa fisicamente os sensores do Linux a cada segundo."""
            if not anim_win.winfo_exists(): return
            
            env = os.environ.copy()
            env["LC_ALL"] = "C" 
            
            proc_job = subprocess.run(["lpstat", "-o", printer_name], capture_output=True, text=True, env=env)
            proc_printer = subprocess.run(["lpstat", "-p", printer_name], capture_output=True, text=True, env=env)
            
            p_status = proc_printer.stdout.lower()
            has_error = "disabled" in p_status or "paused" in p_status or "error" in p_status
            
            if job_id and job_id in proc_job.stdout:
                job_status["state"] = "error" if has_error else "printing"
            else:
                if job_status["state"] in ["waiting", "printing", "error"]:
                    job_status["state"] = "gone"
                    
            if job_status["state"] != "gone":
                anim_win.after(1000, poll_job_status)

        def animate(frame=0):
            if not anim_win.winfo_exists(): return
            
            state = job_status["state"]
            
            # Condição 1: Problema na Impressora (Pausada, engasgada, sem papel)
            if state == "error":
                lbl_status.config(text="⚠️ Impressora com Erro / Sem Papel", foreground=Colors.WARNING)
                anim_win.after(1000 // fps, animate, frame) 
                return
                
            elif state == "gone":
                pct = int((frame / total_frames) * 100)
                if pct < 90: # Cancelou antes de terminar
                    lbl_status.config(text="🚫 Impressão Cancelada", foreground=Colors.DANGER)
                    prog["value"] = 0
                else: # Finalizou
                    lbl_status.config(text="✔ Impressão Concluída", foreground=Colors.ACCENT_2)
                    prog["value"] = 100
                    canvas.move(paper_id, 0, y_step * (total_frames - frame)) 
                    canvas.move(img_id, 0, y_step * (total_frames - frame))
                
                ttk.Button(anim_win, text="Fechar", style="Primary.TButton", command=anim_win.destroy).pack(pady=10)
                return

            if frame <= total_frames:
                canvas.move(paper_id, 0, y_step)
                canvas.move(img_id, 0, y_step)
                
                pct = int((frame / total_frames) * 100)
                prog["value"] = pct
                lbl_status.config(text=f"Imprimindo... {pct}%", foreground=Colors.FG_TEXT)
                
                anim_win.after(1000 // fps, animate, frame + 1)
            else:
                lbl_status.config(text="Finalizando na impressora...", foreground=Colors.FG_TEXT)
                anim_win.after(1000, animate, frame)

        poll_job_status()
        anim_win.after(500, animate)


    def _show_image_preview(path, print_callback):
        try:
            from PIL import Image, ImageTk
        except ImportError: return

        top = tk.Toplevel(app.root)
        top.title("Confirmação de Impressão")
        top.geometry("600x750")
        top.configure(bg=Colors.BG_ROOT)
        top.transient(app.root) 
        top.grab_set() 

        lbl_title = ttk.Label(top, text="Confira sua Imagem", style="Title.TLabel")
        lbl_title.pack(pady=15)

        img = Image.open(path)
        img.thumbnail((500, 550))
        photo = ImageTk.PhotoImage(img)
        
        lbl_img = tk.Label(top, image=photo, bg=Colors.BG_ROOT)
        lbl_img.image = photo 
        lbl_img.pack(pady=10)

        btn_frame = ttk.Frame(top, style="TFrame")
        btn_frame.pack(fill="x", pady=20)
        
        ttk.Button(btn_frame, text="✖ Cancelar", command=top.destroy).pack(side="left", padx=40)
        
        def confirm():
            top.destroy()
            print_callback()

        ttk.Button(btn_frame, text="🖨️ Confirmar e Imprimir", style="Success.TButton", command=confirm).pack(side="right", padx=40)


    def on_print_doc():
        path = filedialog.askopenfilename()
        if path:
            kwargs = _get_print_kwargs()
            base_time = {"Draft": 12, "Normal": 35, "High": 85, "Ultra": 240}
            t_seconds = base_time.get(kwargs["qual"], 40) * int(kwargs["copies"])
            
            def do_print():
                job_id = run_print(app, path, **kwargs)
                app.root.after(0, update_queue)
                if job_id:
                    app.root.after(0, lambda: _show_printing_animation(path, t_seconds, job_id, kwargs["printer"]))

            threading.Thread(target=do_print, daemon=True).start()

    def on_print_img():
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.tiff *.bmp")])
        if path:
            kwargs = _get_print_kwargs()
            kwargs["force_photo"] = True
            
            def do_print():
                t_seconds = 240 * int(kwargs["copies"]) 
                
                def thread_target():
                    job_id = process_and_print_image(app, path, kwargs)
                    app.root.after(0, update_queue)
                    if job_id:
                        app.root.after(0, lambda: _show_printing_animation(path, t_seconds, job_id, kwargs["printer"]))

                threading.Thread(target=thread_target, daemon=True).start()

            _show_image_preview(path, do_print)

    def on_cancel():
        cancel_all_jobs(app, app.var_printer.get())
        update_queue()

    def on_resume():
        resume_printer(app, app.var_printer.get())
        update_queue()

    actions = ttk.Frame(inner, style="Card.TFrame")
    actions.grid(row=10, column=0, columnspan=4, sticky="ew", pady=(18, 0))
    ttk.Button(actions, text="📄 Imprimir Documento", style="Secondary.TButton", command=on_print_doc).pack(side="left")
    ttk.Button(actions, text="🖼️ Imprimir Foto (Masterizada)", style="Primary.TButton", command=on_print_img).pack(side="left", padx=8)
    
    ttk.Button(actions, text="▶️ Destravar Erro", style="Cyan.TButton", command=on_resume).pack(side="right", padx=(8, 0))
    ttk.Button(actions, text="⏸ Cancelar Fila", style="Danger.TButton", command=on_cancel).pack(side="right")

    cols = ("id", "printer", "status")
    app.tree_jobs = ttk.Treeview(inner, columns=cols, show="headings", height=5)
    for c, w, t in [("id", 100, "ID da Fila"), ("printer", 250, "Impressora"), ("status", 350, "Status/Documento")]:
        app.tree_jobs.heading(c, text=t)
        app.tree_jobs.column(c, width=w, anchor="w")
    app.tree_jobs.grid(row=12, column=0, columnspan=4, sticky="ew", pady=(20,0))
    inner.columnconfigure(1, weight=1)
    
    refresh_printers()