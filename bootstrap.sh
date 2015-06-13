sudo apt-add-repository -y ppa:pypy/ppa
sudo apt-get update
sudo apt-get -y install git wget pypy
pip install virtualenv
pip install virtualenvwrapper
mkvirtualenv --no-site-packages --distribute --python=/usr/lib/pypy/bin/pypy-c repl
pip install tornado
wget -qO- https://get.docker.com/ | sh
git clone https://github.com/robobario/repl.git
cd repl
sudo python docker.py
nohup sudo python server.py &
