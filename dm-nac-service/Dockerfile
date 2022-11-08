#
FROM python:3.9.2-alpine

#
WORKDIR /code
RUN mkdir -p ./logs

#
COPY ./requirements.txt /code/requirements.txt

#
RUN  apk add build-base

#
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install 'uvicorn[standard]'
RUN pip install fastapi-utils

#
COPY ./dm_nac_service /code/dm_nac_service

#EXPOSE 3306
#CMD ["uvicorn", "dm_nac_service.main:app", "--host", "0.0.0.0", "--port", "9019"]
CMD ["uvicorn", "dm_nac_service.main:app", "--host", "0.0.0.0", "--port", "9019", "--root-path", "/dm-nac"]
