FROM python:3.7

ARG REQUIREMENTS_FILE=requirements.txt

#
# Install pip-tools and dependencies
#
WORKDIR /code
COPY $REQUIREMENTS_FILE .
RUN pip install -r $REQUIREMENTS_FILE

ENTRYPOINT ["flit"]
