FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 6701
ENTRYPOINT ["python"]
CMD ["app1.py"]
