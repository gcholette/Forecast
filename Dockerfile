FROM python:3.6-stretch


RUN apt-get update && apt-get install -y \
  gcc \
  gfortran \
  g++ \
  build-essential \
  libgrib-api-dev

RUN pip install numpy pyproj arrow requests

RUN git clone https://github.com/jswhit/pygrib.git pygrib && \
  cd pygrib && git checkout tags/v2.0.2rel


COPY setup.cfg ./pygrib/setup.cfg
RUN cd pygrib && python setup.py build && python setup.py install

WORKDIR /app

COPY src/ /app/src

CMD ["python", "/app/src/script.py"]
