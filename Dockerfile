# Baseimage
FROM python:3.12.10-slim-bookworm

# Build arguments
ARG BUILD_DATE
ARG BUILD_COMMIT
ENV BUILD_DATE=${BUILD_DATE}
ENV BUILD_COMMIT=${BUILD_COMMIT}

# Update Packages
RUN apt update
RUN apt upgrade -y
RUN pip install --upgrade pip
# install git
RUN apt-get install build-essential -y


RUN mkdir /CrewAI-Studio

# Install requirements
COPY ./requirements.txt /CrewAI-Studio/requirements.txt
WORKDIR /CrewAI-Studio
RUN pip install -r requirements.txt

# Copy CrewAI-Studio
COPY ./ /CrewAI-Studio/

# Run app
CMD ["streamlit","run","./app/app.py","--server.headless","true"]
EXPOSE 8501
