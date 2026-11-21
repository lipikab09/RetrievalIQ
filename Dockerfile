FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY data ./data
COPY dashboard.py api.py ./
RUN pip install --no-cache-dir .
EXPOSE 8501 8000
CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0"]
