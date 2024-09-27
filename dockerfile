# Dockerfile
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
