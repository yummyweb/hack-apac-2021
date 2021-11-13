FROM python:3.8

RUN mkdir /hack-apac-2021
WORKDIR /hack-apac-2021

COPY requirements.txt .
COPY gunicorn_config.py .
# Copy the rest of the applications
COPY ./app .

RUN pip install -r requirements.txt

# Environment Variables
ENV PYTHONBUFFERED 1 

# Expose port 8000 to allow communication to/from a server
EXPOSE 8001
STOPSIGNAL SIGINT

# CMD ["python", "./app/app.py"]
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
# CMD ["ls"]

# FROM python:3.8

# RUN mkdir -p /deploy/hack-apac-2021

# COPY requirements.txt /deploy/hack-apac-2021/requirements.txt
# RUN pip install -r /deploy/hack-apac-2021/requirements.txt

# # Copy the rest of the applications
# COPY gunicorn_config.py /deploy/hack-apac-2021/gunicorn_config.py
# COPY ./app /deploy/hack-apac-2021

# WORKDIR /deploy/hack-apac-2021

# # Environment Variables
# ENV PYTHONBUFFERED 1
# ENV PYTHONPATH=/hack-apac-2021

# # Expose port 8000 to allow communication to/from a server
# USER 1001
# EXPOSE 8080
# STOPSIGNAL SIGINT

# CMD ["python", "/deploy/hack-apac-2021/app.py"]
# CMD ["ls"]
# # CMD ["gunicorn", "--config", "/deploy/hack-apac-2021/gunicorn_config.py", "app:app"]