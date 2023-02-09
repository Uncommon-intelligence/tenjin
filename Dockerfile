# Use an official Python runtime as the base image
FROM python:3.10-slim

RUN apt update
RUN apt-get install curl make -y
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"


# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app



# Install the dependencies using poetry
RUN poetry install --no-root

# Command to run the application
ENTRYPOINT ["make", "server"]