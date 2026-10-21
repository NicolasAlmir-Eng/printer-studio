import subprocess
import threading
import shutil
import os
from pathlib import Path
from theme import LogLevel

def load_printers():
    proc = subprocess.run(["lpstat", "-e"], capture_output=True, text=True)
    return [p for p in proc.stdout.splitlines() if p.strip()]

def get_queue(printer):
    if not printer: return []
    proc = subprocess.run(["lpstat", "-o", printer], capture_output=True, text=True)
    jobs = []
    for line in proc.stdout.splitlines():
        if line.strip():
            parts = line.split()
            if len(parts) >= 4:
                jobs.append((parts[0], parts[1], " ".join(parts[2:])))
    return jobs

def cancel_all_jobs(app, printer):
    if printer:
        subprocess.run(["cancel", "-a", printer])
        app.log("Fila de impressão completamente limpa.", LogLevel.WARN)

def resume_printer(app, printer):
    if not printer: return
    app.log(f"Enviando comando para limpar erros e acordar '{printer}'...", LogLevel.INFO)
    subprocess.run(["cupsenable", printer])
    subprocess.run(["cupsaccept", printer])
    subprocess.run(["lpadmin", "-p", printer, "-E"])
    app.log("✔ Impressora destravada e pronta para continuar.", LogLevel.OK)

def estimate_print_time(qual, copies):
    base_time = {"Draft": 12, "Normal": 35, "High": 85, "Ultra": 240}
    t_seconds = base_time.get(qual, 40) * int(copies)
    mins, secs = divmod(t_seconds, 60)
    return f"{mins}m {secs}s" if mins > 0 else f"{secs}s"

def run_print(app, path, printer, paper_size, paper_type, qual, color_mode, copies, landscape, borderless, duplex, force_photo=False):
    if not printer: return None
    
    if force_photo:
        paper_type = "Glossy"
        qual = "Ultra"
        color_mode = "Color"
        borderless = True
        
    cups_paper_map = {
        "Photo 10x15": "10x15cm", 
        "Photo 13x18": "13x18cm", 
        "A4": "A4", "A5": "A5", "Letter": "Letter", "Legal": "Legal"
    }
    mapped_size = cups_paper_map.get(paper_size, "A4")
        
    media_val = f"{mapped_size}"
    if paper_type == "Glossy": media_val += ",Premium_Glossy"
    elif paper_type != "Plain": media_val += f",{paper_type}"
        
    cmd = ["lp", "-d", printer, "-o", f"media={media_val}", "-o", f"copies={copies}"]
    
    if qual == "Ultra": 
        cmd.extend(["-o", "print-quality=5", "-o", "printer-resolution=5760x1440dpi", "-o", "Resolution=5760x1440dpi", "-o", "PrinterQuality=Photo"])
    elif qual == "High": cmd.extend(["-o", "print-quality=5"])
    elif qual == "Normal": cmd.extend(["-o", "print-quality=4"])
    elif qual == "Draft": cmd.extend(["-o", "print-quality=3"])

    if color_mode == "Color": cmd.extend(["-o", "ColorModel=RGB"])
    else: cmd.extend(["-o", "ColorModel=KGray"])

    if paper_type == "Glossy": cmd.extend(["-o", "MediaType=PremiumGlossy", "-o", "OutputMode=Photo", "-o", "Ink=Photo"])
    if landscape: cmd.extend(["-o", "landscape"])
    if borderless: cmd.extend(["-o", "Borderless=true", "-o", "PrinterBorderless=true"])
    if duplex: cmd.extend(["-o", "sides=two-sided-long-edge"])

    cmd.extend(["-o", "fit-to-page"])
    cmd.append(path)
    
    app.log(f"Comandos de Impressão: {' '.join(cmd)}", LogLevel.DEBUG)
    
    # Força o terminal em inglês para garantir a leitura do Job ID independente do idioma do Ubuntu
    env = os.environ.copy()
    env["LC_ALL"] = "C"
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    
    est_time = estimate_print_time(qual, copies)
    job_id = None
    
    if proc.returncode == 0:
        # Extrai o ID real do CUPS (Ex: "request id is Printer-L4260-12")
        if "request id is" in proc.stdout:
            job_id = proc.stdout.split("request id is")[1].strip().split()[0]
            
        app.log(f"✔ Arquivo enviado [ID: {job_id}]", LogLevel.OK)
        app.log(f"⏳ Tempo estimado: {est_time}", LogLevel.INFO)
        return job_id
    else:
        app.log(f"Erro ao imprimir: {proc.stderr}", LogLevel.ERR)
        return None

def process_and_print_image(app, path, print_kwargs):
    print_path = path
    if shutil.which("convert"):
        app.log("Executando Masterização Fotográfica...", LogLevel.INFO)
        work_dir = Path(app.config.save_dir)
        work_dir.mkdir(parents=True, exist_ok=True)
        out_file = str(work_dir / f"masterizado_{Path(path).stem}.png")
        
        cmd = ["convert", path, "-modulate", "100,115", "-level", "1%,99%", "-unsharp", "0x2.5+1.5+0", "-density", "600", "-units", "PixelsPerInch", out_file]
        proc = subprocess.run(cmd, capture_output=True)
        if proc.returncode == 0:
            print_path = out_file
            app.log("✔ Masterização concluída.", LogLevel.OK)
            
    return run_print(app, print_path, **print_kwargs)