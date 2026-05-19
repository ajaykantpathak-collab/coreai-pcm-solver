 Start the FastAPI backend engine securely in the background
python solver_service.py &

# Launch the Streamlit frontend interface to the world
streamlit run app.py --server.port 8501 --server.address 0.0.0.0