FROM python:3

COPY main.py /
COPY Pipfile /
COPY Pipfile.lock /
COPY views.csv /

RUN pip install 'pipenv=2018.11.26'
RUN pipenv install --system --deploy

ENTRYPOINT ["pipenv", "run", "python", "./main.py"]