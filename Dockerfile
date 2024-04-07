FROM python:latest

#Installing dependencies
RUN apt-get update
RUN apt-get install -y android-tools-adb
RUN apt-get install -y npm


# Set environment variables for Android SDK
ENV ANDROID_HOME="/opt/android-sdk"
ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
ENV PATH="${PATH}:${ANDROID_HOME}/cmdline-tools/tools/bin:${ANDROID_HOME}/platform-tools"

# Download and extract Android Command Line Tools
RUN wget -q https://dl.google.com/android/repository/commandlinetools-linux-6858069_latest.zip -O /tmp/cmdline-tools.zip \
    && mkdir -p ${ANDROID_HOME}/cmdline-tools \
    && unzip -q /tmp/cmdline-tools.zip -d ${ANDROID_HOME}/cmdline-tools \
    && rm /tmp/cmdline-tools.zip \
    && mv ${ANDROID_HOME}/cmdline-tools/cmdline-tools ${ANDROID_HOME}/cmdline-tools/tools

# Accept Android SDK licenses
RUN yes | sdkmanager --licenses

# Install Android SDK components: build-tools and platform-tools
RUN sdkmanager --install "build-tools;31.0.0" platform-tools

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
