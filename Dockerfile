FROM python:3

COPY main.py /
COPY Pipfile /
COPY Pipfile.lock /
COPY views.csv /

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile
RUN pipenv shell

ENTRYPOINT ["pipenv", "run", "python", "./main.py"]