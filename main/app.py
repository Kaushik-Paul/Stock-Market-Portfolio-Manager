import os
import sys

# Ensure project root is on sys.path for `main.*` imports when running directly.
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from main.gradio_ui.builder import create_ui as build_ui

if __name__ == "__main__":
    ui = build_ui()
    ui.launch()
