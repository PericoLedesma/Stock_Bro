FROM python:3.11-slim

# Set working directory
WORKDIR /app


# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8500

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8500/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8500", "--server.address=0.0.0.0"]
