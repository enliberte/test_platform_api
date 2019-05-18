FROM python:3.7
ADD . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "api.py"]