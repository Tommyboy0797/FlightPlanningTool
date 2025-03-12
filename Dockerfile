FROM python:3.13

# Set working directory
WORKDIR /app/

# Copy requirements file to container 
COPY ./requirements.txt /app/requirements.txt

# Install required packages
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Add database directory
COPY ./database /app/database

# Add Backend directory
COPY ./Backend /app/Backend

# Add Frontend directory
COPY ./Frontend /app/Frontend

# Add static directory
COPY ./static /app/static

# Add server.py to root
ADD server.py ./

# Set default command that should be executed when container starts up
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]