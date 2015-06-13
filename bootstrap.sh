sudo apt-add-repository -y ppa:pypy/ppa
sudo apt-get update
sudo apt-get -y install git wget pypy python-pip
sudo pip install virtualenv
sudo pip install virtualenvwrapper
mkvirtualenv --no-site-packages --distribute --python=/usr/lib/pypy/bin/pypy-c repl
pip install tornado
command -v docker >/dev/null 2>&1 && wget -qO- https://get.docker.com/ | sh
git clone https://github.com/robobario/repl.git
cd repl
sudo python docker.py
nohup sudo python server.py &
