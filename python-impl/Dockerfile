FROM python:3.6-stretch as base


RUN apt-get update && apt-get install -y \
  gcc \
  gfortran \
  g++ \
  build-essential \
  libgrib-api-dev \
  cython

RUN pip install numpy pyproj arrow requests pygrib

# RUN git clone https://github.com/jswhit/pygrib.git pygrib && \
#   cd pygrib && git checkout tags/v2.1.4rel

# COPY setup.cfg ./pygrib/setup.cfg
# RUN cd pygrib && python setup.py build && python setup.py install

WORKDIR /app

COPY src/ /app/src

FROM base as test
CMD ["python", "/app/src/tests.py"]

FROM base as prod
CMD ["python", "/app/src/script.py"]
