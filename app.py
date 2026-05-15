from main.app import ensure_uvx
from main.gradio_ui.builder import LAUNCH_KWARGS, create_ui

ensure_uvx()
demo = create_ui()

if __name__ == "__main__":
    demo.launch(**LAUNCH_KWARGS)
