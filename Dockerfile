FROM appium/appium:latest

#Installing dependencies
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y android-tools-adb
RUN apt-get install -y npm

#Installing appium 
RUN npm install -g appium
RUN appium driver install uiautomator2

#Installing Python dependencies
RUN pip install appium-python-client flask requests

#Setting working directory
WORKDIR /app

COPY . .

#Starting application
ENTRYPOINT ["python","api.py"]
