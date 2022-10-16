FROM python:3.8


# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt
# Copy app code and set working directory
COPY . .
WORKDIR /

# Run
CMD [ "python3" , "backend/app.py"]