@echo off
echo Starting Marvel Streamlit App...
echo.
echo Make sure you have:
echo 1. Installed all requirements: pip install -r requirements.txt streamlit
echo 2. Started Ollama: ollama serve
echo 3. Pulled Mistral model: ollama pull mistral:7b
echo.
pause
streamlit run marvel_streamlit_app.py

