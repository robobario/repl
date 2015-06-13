sudo apt-get update
sudo apt-get install git wget
wget -qO- https://get.docker.com/ | sh
git clone https://github.com/robobario/repl.git
cd repl
sudo python docker.py
nohup sudo python server.py &
