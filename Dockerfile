FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install .

WORKDIR /src

ENTRYPOINT [ "melthon" ]
CMD [ "--help" ]