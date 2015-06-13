apt-get update
apt-get install git
apt-get install wget
wget -qO- https://get.docker.com/ | sh
git clone https://github.com/robobario/repl.git
cd repl
python docker.py
nohup python server.py &
