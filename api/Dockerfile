FROM python:3.6
ENV PYTHONUNBUFFERED 0
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt
ADD . /usr/src/app/
CMD ["python", "api.py"]
