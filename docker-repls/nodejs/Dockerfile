FROM ubuntu
RUN apt-get update && apt-get install -y curl && apt-get clean && curl -sL https://deb.nodesource.com/setup_0.12 | sudo bash - && sudo apt-get install -y nodejs
CMD ["node"]

