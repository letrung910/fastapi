ARG PYTHONVERSION="3.11"
###############################
# builder stage
###############################
FROM python:${PYTHONVERSION}-slim as builder
ARG PYTHONVERSION

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

############################
# runner stage
# ############################
FROM python:${PYTHONVERSION}-slim as runner
ARG PYTHONVERSION

WORKDIR /code
COPY --from=builder /usr/local/bin/python /usr/local/bin/python
COPY --from=builder /usr/local/bin/pip /usr/local/bin/pip
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=builder /usr/local/bin/alembic /usr/local/bin/alembic

COPY --from=builder /usr/local/lib/python${PYTHONVERSION}/site-packages /usr/local/lib/python${PYTHONVERSION}/site-packages
COPY ./app /code/app
WORKDIR /code/app

CMD ["uvicorn", "main:app", "--workers", "4", "--host", "0.0.0.0", "--port", "80"]