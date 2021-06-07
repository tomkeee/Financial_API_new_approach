FROM python:3.9.4
ENV PYTHONUNBUFFERED=1
WORKDIR /docker
COPY . /docker
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]