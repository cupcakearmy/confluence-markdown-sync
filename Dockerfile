FROM python:3.10-alpine

WORKDIR /action

COPY ./Pipfile* ./
RUN pip install pipenv && \
  pipenv install --system --deploy && \
  pipenv --clear

COPY ./src .

ENTRYPOINT [ "python" ]
CMD [ "/action/main.py" ]
