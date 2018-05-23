FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD customersvc /code/customersvc
ADD migrations /code/migrations
ADD tests /code/tests
ADD db_migrate.sh /code/
ENTRYPOINT ["python", "-m", "customersvc.app"]
