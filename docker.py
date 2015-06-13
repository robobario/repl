import os.path
import os
import subprocess

initial_dir = os.getcwd()
script_dir = os.path.dirname(os.path.realpath(__file__))
repl_dir = os.path.join(script_dir, "docker-repls")
for filename in os.listdir(repl_dir):
  a_repl = os.path.join(repl_dir,filename)
  if os.path.isdir(a_repl):
    os.chdir(a_repl)
    subprocess.call(["docker","build","-t",filename,"."])


