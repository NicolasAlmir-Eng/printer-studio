import subprocess
import threading
import shutil
from tkinter import messagebox
from theme import LogLevel

def check_dependencies(log_func):
    req = {"scanimage": "sane-utils", "lp": "cups-client", "airscan-discover": "sane-airscan"}
    missing = [t for t in req if not shutil.which(t)]
    if missing: log_func(f"Atenção: Instale: {' '.join(missing)}", LogLevel.WARN)
    if not shutil.which("tesseract"): log_func("OCR (Tesseract) não instalado.", LogLevel.WARN)
    if not shutil.which("mogrify"): log_func("Auto-Trim (ImageMagick) não instalado.", LogLevel.WARN)

def discover_scanners(app, var_device):
    app.log("Buscando scanners na rede...", LogLevel.INFO)
    def run():
        proc = subprocess.run(["airscan-discover"], capture_output=True, text=True)
        for line in proc.stdout.splitlines():
            if "eSCL" in line and "http" in line:
                url = line.split("=", 1)[1].split(",")[0].strip()
                app.root.after(0, var_device.set, f"escl:{url}")
                app.log(f"Scanner encontrado: escl:{url}", LogLevel.OK)
                return
    threading.Thread(target=run, daemon=True).start()

def run_head_cleaning(app):
    if messagebox.askyesno("Limpeza", "Isso consumirá tinta. A impressora deve estar via USB. Continuar?"):
        app.log("Enviando comando de limpeza para USB...", LogLevel.INFO)
        threading.Thread(target=lambda: subprocess.run(["sudo", "escputil", "-c", "-u", "-r", "/dev/usb/lp0"]), daemon=True).start()

def run_nozzle_check(app):
    app.log("Imprimindo teste de verificação de jatos...", LogLevel.INFO)
    threading.Thread(target=lambda: subprocess.run(["sudo", "escputil", "-n", "-u", "-r", "/dev/usb/lp0"]), daemon=True).start()

def check_ink_usb(app):
    try:
        res = subprocess.run(["sudo", "escputil", "-i", "-u", "-r", "/dev/usb/lp0"], capture_output=True, text=True)
        app.log(f"Nível USB:\n{res.stdout}", LogLevel.OK)
        if res.stderr: app.log(res.stderr, LogLevel.WARN)
    except Exception as e:
        app.log(f"Falha ao checar USB: {e}", LogLevel.ERR)
