import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List

CONFIG_DIR = Path.home() / ".config" / "epson_studio"
CONFIG_FILE = CONFIG_DIR / "settings.json"
PROFILES_FILE = CONFIG_DIR / "profiles.json"
HISTORY_FILE = CONFIG_DIR / "history.json"
SCAN_DIR_DEFAULT = Path.home() / "Documentos" / "PrinterScans"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class AppConfig:
    scanner_device: str = "escl:https://192.168.100.13:443"
    dpi: str = "300"
    color_mode: str = "Color"
    paper_size: str = "A4"
    paper_type: str = "Glossy"
    last_printer: str = ""
    save_dir: str = str(SCAN_DIR_DEFAULT)
    auto_open_after_scan: bool = False
    duplex: bool = False
    ocr_enabled: bool = False
    auto_trim: bool = False

    print_quality: str = "Ultra"
    print_dpi: str = "600"
    color_print_mode: str = "Color"
    borderless: bool = True
    auto_rotate: bool = True
    fit_to_page: bool = True

    @classmethod
    def load(cls) -> "AppConfig":
        if CONFIG_FILE.exists():
            try:
                data = json.loads(CONFIG_FILE.read_text())
                return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
            except Exception:
                pass
        return cls()

    def save(self) -> None:
        try:
            CONFIG_FILE.write_text(json.dumps(asdict(self), indent=2))
        except Exception:
            pass

@dataclass
class PrintProfile:
    name: str
    paper_size: str
    paper_type: str
    quality: str
    color_mode: str
    duplex: bool = False
    landscape: bool = False
    borderless: bool = False

@dataclass
class HistoryEntry:
    timestamp: str
    action: str
    target: str
    file: str
    detail: str = ""
    status: str = "OK"

class ProfileManager:
    def __init__(self):
        self.profiles: List[PrintProfile] = []
        self.load()

    def load(self):
        if PROFILES_FILE.exists():
            try:
                raw = json.loads(PROFILES_FILE.read_text())
                self.profiles = [PrintProfile(**p) for p in raw]
            except Exception:
                self.profiles = []
        if not self.profiles:
            self.profiles = [
                PrintProfile("Foto Ultra", "Photo 10x15", "Glossy", "Ultra", "Color", borderless=True),
            ]
            self.save()

    def save(self):
        try:
            PROFILES_FILE.write_text(json.dumps([asdict(p) for p in self.profiles], indent=2))
        except Exception: pass

class HistoryManager:
    MAX = 200
    def __init__(self):
        self.entries: List[HistoryEntry] = []
        self.load()

    def load(self):
        if HISTORY_FILE.exists():
            try:
                raw = json.loads(HISTORY_FILE.read_text())
                self.entries = [HistoryEntry(**e) for e in raw]
            except Exception: self.entries = []
