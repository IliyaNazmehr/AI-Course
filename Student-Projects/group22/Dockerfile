# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for Tesseract and other libraries
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-fas \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/* \
    && find /usr/share/tesseract-ocr/ -type f

# Set Tesseract data directory environment variable
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (Railway assigns the port)
EXPOSE 8000

# Run the bot
CMD ["python", "bot.py"]