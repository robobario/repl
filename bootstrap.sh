sudo apt-add-repository -y ppa:pypy/ppa
sudo apt-get update
sudo apt-get -y install git wget pypy python-pip build-essential python-dev
sudo pip install virtualenv
sudo pip install virtualenvwrapper
mkvirtualenv --no-site-packages --distribute --python=/usr/lib/pypy/bin/pypy-c repl
workon repl
pip install tornado
command -v docker >/dev/null 2>&1 || wget -qO- https://get.docker.com/ | sh
sudo usermod -aG docker $USER
git clone https://github.com/robobario/repl.git
cd repl
sudo python docker.py
