FROM ubuntu
RUN apt-get update && apt-get -y install wget default-jre \
  && apt-get autoremove && apt-get clean \
  && wget -q -O /opt/clojure.jar http://repo1.maven.org/maven2/org/clojure/clojure/1.6.0/clojure-1.6.0.jar
CMD ["java -jar /opt/clojure.jar"]

