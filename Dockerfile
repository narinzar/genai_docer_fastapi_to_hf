# Use Python 3.9 as the base image
# This provides us with a compatible Python version for our dependencies
FROM python:3.9

# Set the working directory inside the container
# This is a temporary directory for initial setup
WORKDIR /code

# Copy only the requirements file first
# This leverages Docker's cache - if requirements don't change, 
# this layer won't be rebuilt in subsequent builds
COPY ./requirements.txt /code/requirements.txt

# Install Python dependencies
# --no-cache-dir: Don't store the package cache, reduces image size
# --upgrade: Makes sure we get the latest compatible versions
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Create a non-root user for security
# Running as non-root is a security best practice to limit container privileges
RUN useradd user

# Switch to the non-root user
# All subsequent commands will run as this user, not as root
USER user

# Set environment variables
# HOME: Defines the home directory for the user
# PATH: Adds the user's local bin directory to the PATH for command accessibility
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH 

# Set the working directory to the user's home directory
# This is where our application code will reside
WORKDIR $HOME/app

# Copy the application code into the container
# --chown=user:user: Sets the proper ownership of the files
# The '.' means "copy everything from the current directory on the host"
COPY --chown=user:user . $HOME/app

# Command to run when the container starts
# uvicorn: ASGI server for FastAPI
# app:app: The format is "module:instance" - app.py file and app variable
# --host 0.0.0.0: Accept connections from any IP
# --port 7860: Listen on port 7860
# --reload: Auto-reload on code changes (good for development, can be removed for production)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--reload"]