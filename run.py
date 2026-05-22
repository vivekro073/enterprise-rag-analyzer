import subprocess
import sys
import time


def start_servers():
    print("🚀 Booting up Enterprise RAG Architecture...")

    # 1. Start the FastAPI backend
    print("🟢 Starting FastAPI Backend on port 8000...")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"]
    )

    # Give the backend 2 seconds to fully load before hitting it with the frontend
    time.sleep(2)

    # 2. Start the Streamlit frontend
    print("🔵 Starting Streamlit Frontend...")
    frontend = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py"]
    )

    try:
        # Keep the script running so your servers don't turn off
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        # If you hit the Stop button in your IDE, this cleanly shuts everything down
        print("\n🛑 Shutting down all servers...")
        backend.terminate()
        frontend.terminate()


if __name__ == "__main__":
    start_servers()