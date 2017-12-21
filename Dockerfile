FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code/z_rank
ADD requirements.txt /code/z_rank/
WORKDIR /code/z_rank
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
ADD . /code/z_rank/
