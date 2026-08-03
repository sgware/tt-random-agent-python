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

# Set `/app` as the working directory.
WORKDIR /app

#-------------------------------------------------------------------------------
# Development Phase
# The instructions in this section only run if you build the image with
# `--target dev`. Put instructions here that should only run when you are
# testing and developing the image. This section assumes there is a container
# named `tt-web` running as a test version of the Tandem Tales web server.
#-------------------------------------------------------------------------------
FROM base AS dev

# Run the development version of the entrypoint script and keep the shell open.
CMD ["sh", "-c", "trap 'exec bash' INT; /app/run.dev.sh; exec bash"]

#-------------------------------------------------------------------------------
# Production Phase
# The instructions in this section run if you build the image with
# `--target prod`. Since this is the last phase defined, these instructions will
# run by default if you don't specify a target. Put instructions here that
# should only run in the final, working version of your image.
#-------------------------------------------------------------------------------
FROM base AS prod

# Run the production version of the entrypoint script.
CMD ["sh", "-c", "/app/run.prod.sh"]