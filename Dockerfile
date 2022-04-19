FROM python:3.10

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
ADD src/main.py /main.py

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "/main.py" ]