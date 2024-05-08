# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /src

# Set the working directory in the container
WORKDIR /scr
ADD . /src
# Install any needed dependencies specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install fastapi    
RUN pip install uvicorn
RUN pip install pandas
RUN pip install numpy
RUN pip install scikit-learn
RUN pip install requests

COPY . /scr/
# Run the FastAPI application with Uvicorn
CMD ["python", "app_model.py"]

# Expose the port the app runs on
EXPOSE 8000