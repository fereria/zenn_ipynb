FROM python:3.7-slim
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

ADD ./requirements.txt /work_dir/
ADD ./jupyter_notebook_config.py /tmp/

RUN mv /tmp/jupyter_notebook_config.py ./~jupyter

WORKDIR /work_dir
RUN pip install -r requirements.txt

EXPOSE 8888