import sys
from typing import Optional


def runner(temp_file: str, port: Optional[str] = None):
    import importlib

    # Start streaming application
    port = port or "8501"
    streamlit_cli = importlib.import_module("streamlit.web.cli")
    sys.argv = ["streamlit", "run", temp_file, "--server.port", port]
    streamlit_cli.main()
