import subprocess
import threading
import shutil
from pathlib import Path
from tkinter import messagebox
from theme import LogLevel

def _run_post_processing(app, file_path, use_trim, use_ocr):
    if use_trim and shutil.which("mogrify"):
        app.log(f"Aplicando recorte automático em: {Path(file_path).name}", LogLevel.INFO)
        subprocess.run(["mogrify", "-fuzz", "10%", "-trim", "+repage", file_path])
    
    if use_ocr and shutil.which("tesseract"):
        base_out = str(file_path).rsplit('.', 1)[0]
        app.log(f"Lendo texto com Inteligência Artificial (OCR)...", LogLevel.INFO)
        proc = subprocess.run(["tesseract", file_path, base_out, "-l", "por+eng"], capture_output=True)
        if proc.returncode == 0:
            app.log(f"✔ Texto extraído salvo em: {Path(base_out).name}.txt", LogLevel.OK)

def run_scan(app, out_path, device, color, dpi, use_trim, use_ocr, auto_open) -> bool:
    fmt = "pdf" if out_path.endswith(".pdf") else "png"
    cmd = ["scanimage", "-d", device, f"--format={fmt}", f"--mode={color}", f"--resolution={dpi}", "-o", out_path]
    
    app.log(f"Digitalizando documento...", LogLevel.INFO)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0:
        _run_post_processing(app, out_path, use_trim, use_ocr)
        if auto_open: 
            subprocess.Popen(["xdg-open", out_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    else:
        app.log(f"Erro no scanner: {proc.stderr}", LogLevel.ERR)
        return False

def start_scan_job(app, path, device, color, dpi, use_trim, use_ocr, auto_open):
    app.set_busy(True)
    def run():
        run_scan(app, path, device, color, dpi, use_trim, use_ocr, auto_open)
        app.root.after(0, app.set_busy, False)
    threading.Thread(target=run, daemon=True).start()

def start_multi_scan_job(app, out_pdf, savedir, device, color, dpi, use_trim, use_ocr):
    app.set_busy(True)
    def run():
        tmp1 = str(Path(savedir) / "tmp_1.png")
        tmp2 = str(Path(savedir) / "tmp_2.png")
        if run_scan(app, tmp1, device, color, dpi, use_trim, use_ocr, False):
            messagebox.showinfo("Próxima", "Coloque a próxima página e clique OK")
            if run_scan(app, tmp2, device, color, dpi, use_trim, use_ocr, False):
                subprocess.run(["img2pdf", tmp1, tmp2, "-o", out_pdf])
                app.log("PDF Múltiplo gerado com sucesso!", LogLevel.OK)
        app.root.after(0, app.set_busy, False)
    threading.Thread(target=run, daemon=True).start()
