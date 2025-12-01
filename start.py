import subprocess
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_PYTHON = ROOT / "venv" / "Scripts" / "python.exe"
VENV_STREAMLIT = ROOT / "venv" / "Scripts" / "streamlit.exe"

print("Starte Docker Compose...")
subprocess.Popen(["docker-compose", "up", "-d"]).wait()
time.sleep(5)

print("Starte Producer...")
subprocess.Popen([str(VENV_PYTHON), "-m", "producer.producer_stocks"])

print("Starte Consumer...")
subprocess.Popen([str(VENV_PYTHON), "-m", "consumers.consumer"])

print("Starte Streamlit...")
subprocess.Popen([str(VENV_STREAMLIT), "run", "dashboard/app.py"])

print("Alles gestartet!")
