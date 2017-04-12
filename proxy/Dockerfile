FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 12345
ENTRYPOINT ["python"]
CMD ["proxy.py"]
