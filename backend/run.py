if __name__ == "__main__":
    import os
    import sys
    try:
        import uvicorn
    except Exception:
        print("Error: required package 'uvicorn' is not installed.")
        print("Install dependencies with: pip install -r requirements.txt")
        print("Or install just uvicorn: pip install 'uvicorn[standard]'")
        print(r"If you use a virtual environment, activate it first (e.g. .\.venv\Scripts\Activate.ps1).")
        sys.exit(1)

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

    display_host = HOST if HOST != "0.0.0.0" else "localhost"
    app_url = f"http://{display_host}:{PORT}"
    docs_url = f"{app_url}/docs"

    print("Starting Gerenciador de Estoque (development mode)")
    print(f"App: {app_url}")
    print(f"Docs: {docs_url}")

    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
