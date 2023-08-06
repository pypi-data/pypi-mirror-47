# Ansible IPLB Module

The aim of this repository is to provide an ansible module for handling ovh iplb

## Dev part

For CI, if you have docker, you can run `make ci`.
If you want something faster or don't want to run test using docker, you should use pyenv:
```
pyenv install $(make echo_py3_version)
pyenv virtualenv $(make echo_py3_version) ansible_iplb_py3
pyenv activate ansible_iplb_py3
pip install -r requirements/dev.txt
make test style
```

For python2, do same command replacing py3 by py2

You can also run your module against real ovh api v6.
For that create a .env file with the following content:
```
SECRET_PATH_STORE=me/apiovh/token
LOAD_BALANCER=loadbalancer-xxxxxxxxxxxxxxxxxxxx
```
Or if you don't use pass:
```
LOAD_BALANCER=loadbalancer-c6f9b9aa43f6cc17bd51964011f48d76
OVH_APPLICATION_KEY=xxxxxxxxxxxx
OVH_APPLICATION_SECRET=xxxxxxxxxxxx
OVH_CONSUMER_KEY=xxxxxxxxxxxx
```

Those secrets will be used to populate the gomplate template `args.json`.
You can adapt it to test what you want.
Run your code with:
```
make run
```

# Installation part
```
pip install --extra-index-url https://pypi.ovh.net/simple ansible-iplb
```
