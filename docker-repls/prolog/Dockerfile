FROM ubuntu
RUN apt-get update && apt-get install -y software-properties-common && apt-add-repository -y ppa:swi-prolog/stable && sudo apt-get update && apt-get -y install swi-prolog && apt-get clean
CMD ["swipl"]

