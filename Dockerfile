FROM python:3.9-slim-buster as stage-app
#FROM python:latest as stage-app


COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install --upgrade pip
COPY . code
WORKDIR /code
#RUN python manage.py runserver

#CMD ["gunicorn", "--config", "gunicorn.conf.py", "dentist:website"]

# Expose ports
EXPOSE 8000

# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
#