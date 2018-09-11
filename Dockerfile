FROM jbarlow83/ocrmypdf
USER root
RUN pip3 install --upgrade setuptools
RUN pip3 install Flask
RUN mkdir /code
WORKDIR /code
ADD . /code