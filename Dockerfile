FROM python:latest

#Installing dependencies
RUN apt-get update
RUN apt-get install -y android-tools-adb
RUN apt-get install -y npm

#Installing appium 
RUN npm install -g appium
RUN appium driver install uiautomator2

#Installing Python dependencies
RUN pip install appium-python-client flask

#Setting working directory
WORKDIR /app

COPY . .

#Starting appium servers in background
CMD appium --port 4723 --allow-insecure=Adb-shell &
CMD appium --port 4724 --allow-insecure=Adb-shell &
ENTRYPOINT ["python","api.py"]