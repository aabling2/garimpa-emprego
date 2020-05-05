FROM python:3.7.7
COPY ./requirements.txt /Garimpa_emprego/requirements.txt
COPY . /Garimpa_emprego
WORKDIR /Garimpa_emprego
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["main.py"]