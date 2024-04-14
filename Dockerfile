FROM python:latest
#================================================
# Set environment variables for Android SDK and Java
ENV ADB_HOME="/usr/bin/"
ENV ANDROID_HOME="/opt/android/"
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-arm64"
ENV PATH="${PATH}:${ANDROID_HOME}/cmdline-tools/tools/bin:${ANDROID_HOME}/platform-tools:${JAVA_HOME}/bin:${ADB_HOME}"
#Installing dependencies
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y npm
RUN apt-get install -y usbutils
RUN apt-get install -y net-tools
# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*
# Download and extract Android Command Line Tools
RUN wget -q https://dl.google.com/android/repository/commandlinetools-linux-6858069_latest.zip -O /tmp/cmdline-tools.zip \
    && mkdir -p ${ANDROID_HOME}/cmdline-tools \
    && unzip -q /tmp/cmdline-tools.zip -d ${ANDROID_HOME}/cmdline-tools \
    && rm /tmp/cmdline-tools.zip \
    && mv ${ANDROID_HOME}/cmdline-tools/cmdline-tools ${ANDROID_HOME}/cmdline-tools/tools
# Accept Android SDK licenses
RUN yes | sdkmanager --licenses
# Install Android SDK components: build-tools and platform-tools
#RUN sdkmanager --install "build-tools;34.0.0" platform-tools
#Installing appium 
RUN npm install -g appium
RUN appium driver install uiautomator2
#Installing Python dependencies
RUN pip install appium-python-client flask requests common-io-python
#Setting working directory
WORKDIR /app
COPY . .
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y android-tools-adb
RUN chmod a+x startAppiumServers
RUN mkdir /opt/android/platform-tools/
RUN ln -s /usr/bin/adb /opt/android/platform-tools/adb
#Starting application
ENTRYPOINT ["python","api.py"]
