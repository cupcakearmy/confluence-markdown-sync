FROM python:3.9-alpine

WORKDIR /tmp
RUN pip install pipenv
COPY ./Pipfile* ./
RUN pipenv install --system --deploy


WORKDIR /action
COPY ./src .

ENTRYPOINT [ "python" ]
CMD [ "/action/main.py" ]