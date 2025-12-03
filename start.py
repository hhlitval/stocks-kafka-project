import subprocess
import time
from pathlib import Path
from utils import load_historical_data, is_market_open, load_json, get_path

ROOT = Path(__file__).resolve().parent
VENV_PYTHON = ROOT / "venv" / "Scripts" / "python.exe"
VENV_STREAMLIT = ROOT / "venv" / "Scripts" / "streamlit.exe"
symbols = load_json(get_path("config", "symbols.json"))["symbols"]

if is_market_open():
  print("Starte Docker Compose...")
  subprocess.Popen(["docker-compose", "up", "-d"]).wait()
  time.sleep(5)

  print("Starte Producer...")
  subprocess.Popen([str(VENV_PYTHON), "-m", "producer.producer_stocks"])
  # subprocess.Popen(["python", "-m", "producer.producer_stocks"])

  print("Starte Consumer...")
  subprocess.Popen([str(VENV_PYTHON), "-m", "consumers.consumer"])  
  # subprocess.Popen(["python", "-m", "consumers.consumer"])
else:
  print("Lade historische Daten...")
  load_historical_data(symbols)

print("Starte Streamlit...")
# subprocess.Popen(["streamlit", "run", "dashboard/app.py"])