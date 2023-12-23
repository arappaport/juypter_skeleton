python3 -m venv $(basename $PWD)
source $(basename $PWD)/bin/activate
pip3 install -r requirements.txt
ipython kernel install --user --name=$(basename $PWD)