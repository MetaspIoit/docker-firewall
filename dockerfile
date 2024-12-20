# Use a lightweight Python image
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y tcpdump iptables

# Copy the script into the container
COPY detect_port_scanning.py /app/detect_port_scanning.py

# Set the working directory
WORKDIR /app

# Install Python dependencies if required
RUN pip install --no-cache-dir -r requirements.txt || true

# Make the script executable
RUN chmod +x /app/detect_port_scanning.py

# Run the script
CMD ["python3", "/app/detect_port_scanning.py"]
