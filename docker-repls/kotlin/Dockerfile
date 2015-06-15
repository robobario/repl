FROM java:8-jre
RUN wget -O /opt/kotlin.zip https://github.com/JetBrains/kotlin/releases/download/build-0.12.200/kotlin-compiler-0.12.200.zip \
  && cd /opt && unzip /opt/kotlin.zip
CMD ["/opt/kotlinc/bin/kotlinc"]

