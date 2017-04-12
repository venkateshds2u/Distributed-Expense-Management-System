FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 9090
ENTRYPOINT ["python"]
CMD ["app3.py"]
