# This file defines the Docker container that will contain the Crawler app.
# From the source image #python
FROM python:3.6-slim
# Identify maintainer
LABEL maintainer = "ncadapen1@gmail.com"
# Set the default working directory
WORKDIR /app/
COPY villefr_api.py requirements.txt city.list.json /app/
RUN pip3	 install -r requirements.txt
CMD ["python","./villefr_api.py"]
# When the container starts, run this
ENTRYPOINT python ./villefr_api.py
