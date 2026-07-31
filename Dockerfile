#===============================================================================
# Tandem Tales Agent (Python) Docker Image
# 
# This Dockerfile defines a container (a lightweight virtual machine) that
# includes an operating system, the Python interpreter, the Tandem Tales Python
# Client library, and the source code for a Tandem Tales agent.
#===============================================================================

#-------------------------------------------------------------------------------
# Base Phase
# The instructions in this section always run.
#-------------------------------------------------------------------------------
# Start with Linux that has Python already installed.
FROM python:3.14 AS base

# Update packages.
RUN apt update
# Git downloads the Tandem Tales Python library.
RUN apt install -y git
# Clean up after installing software.
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

# Install the Tandem Tales Python client library from GitHub.
RUN pip install git+https://github.com/sgware/tt-client-python

# Copy the agent's files into the image.
COPY ./root /

# Ensure Python prints output to the console.
ENV PYTHONUNBUFFERED=1

# Go to `/app` and run `main.py` when the container starts.
WORKDIR /app
CMD ["python3", "main.py"]

#-------------------------------------------------------------------------------
# Development Phase
# The instructions in this section only run if you build the image with
# `--target dev`. Put instructions here that should only run when you are
# testing and developing the image. This section assumes there is a container
# named `tt-web` running as a test version of the Tandem Tales web server.
#-------------------------------------------------------------------------------
FROM base AS dev

# Use the server's public key.
ENV SSL_CERT_FILE=/etc/tt/certs/tt-fullchain.pem

# Run the agent, but keep the bash shell open after it closes.
CMD ["bash", "-c", "python3 main.py; bash"]

#-------------------------------------------------------------------------------
# Production Phase
# The instructions in this section run if you build the image with
# `--target prod`. Since this is the last phase defined, these instructions will
# run by default if you don't specify a target. Put instructions here that
# should only run in the final, working version of your image.
#-------------------------------------------------------------------------------
FROM base AS prod

# This section is empty, but it exists in case it is needed in the future.