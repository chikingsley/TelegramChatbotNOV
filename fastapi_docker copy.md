## Dockerfile Guide

In the same project directory, create a file named `Dockerfile` with the following content:

```Dockerfile
# Start from the official Python base image
FROM python:3.9

# Set the current working directory to /code
WORKDIR /code

# Copy only the requirements file to leverage Docker cache for faster builds
COPY ./requirements.txt /code/requirements.txt

# Install package dependencies listed in requirements.txt
# --no-cache-dir option prevents storing unnecessary cached packages
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the ./app directory inside the /code directory
COPY ./app /code/app

# Set the command to start FastAPI using Uvicorn on port 80
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

**Explanation of Each Step:**
• **FROM python:3.9**
Start with the official Python 3.9 base image.

• **WORKDIR /code**
Sets the current working directory to /code, where the requirements and app files will be stored.

• **COPY ./requirements.txt /code/requirements.txt**
Only the requirements file is copied to leverage Docker’s caching mechanism.

As this file doesn’t change often, Docker can cache this layer, optimizing build times.

• **RUN pip install –no-cache-dir –upgrade -r /code/requirements.txt**
Installs the package dependencies specified in requirements.txt.
--no-cache-dir: Prevents pip from saving downloaded packages locally, saving space.
--upgrade: Ensures any pre-existing packages are updated.
By caching this step, Docker avoids re-downloading and reinstalling packages each time, saving time during development.

• **COPY ./app /code/app**
Copies the application code inside the /code directory.
Since this is the most frequently changing part of the project, placing this step at the end minimizes cache invalidation, speeding up subsequent builds.

• **CMD [“fastapi”, “run”, “app/main.py”, “–port”, “80”]**
Specifies the command to run the FastAPI app using Uvicorn on port 80.
CMD accepts a list format for the command and executes it in the working directory (/code).