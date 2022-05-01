FROM python:3.8

WORKDIR /RestApi

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY /RestApi /RestApi

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["run_app.py"]