@echo off
echo ========================================
echo VideoAsset Manualize - UI Startup
echo ========================================
echo.
echo Starting Streamlit UI...
set PYTHONPATH=src
python -m streamlit run streamlit_app.py
pause
