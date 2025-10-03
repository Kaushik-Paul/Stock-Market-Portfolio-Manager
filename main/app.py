import os
import sys
import shutil
import subprocess

# Ensure project root is on sys.path for `main.*` imports when running directly.
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from main.gradio_ui.builder import create_ui as build_ui

def ensure_uvx():
    try:
        if not os.environ.get("SPACE_ID"):
            return
        if shutil.which("uvx") is None:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "uv"])
    except Exception as e:
        print(f"Warning: could not ensure uvx is installed: {e}")

if __name__ == "__main__":
    ensure_uvx()
    ui = build_ui()
    ui.launch()
