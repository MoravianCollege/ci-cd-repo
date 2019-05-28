# ci-cd-repo

This repo contains a minimal project that utilizes continuous integration
and continuous deployment for a Flask-based app with a single endpoint.  This means:

* When a developer creates a Pull Request, tests are run by the CI server.
* When a Pull Request is merged, tests run, and then the production server is updated.

## Assumptions

* The deployment server is accessible from the web via port 22 (SSH)
* You have the `travis` CLI installed and have logged in using `travis login --pro`


## Initial Server Setup

* Install requirements globally:  `sudo pip3 install -r requirements.txt`
* Install `gunicorn` globally: `sudo pip3 install gunicorn`
* Install the package globally and editable: `pip3 install -e .`  Editable is important because the deploy 
step will use `git pull` to update the source code.
* Find the line in `scripts/cicd.service` that starts `ExecStart=`  The rest of this line is the command to launch
the server.  Using `sudo`, run this command to ensure the server starts correctly and is accessible remotely.  In a
web browser, point to `<IP>/go`, and you should receive `Hello, World!`  Terminate the server.
* Copy `scripts/cicd.service` to `/etc/systemd/system/`
* Run `sudo systemctl start cicd` and verify that the server is accessible.
* Run `sudo systemctl stop cicd` and verify that the server is no longer accessible.
* Run `sudo systemctl enable cicd`
* Reboot and verify that the server is accessible.


## Continuous Integration Setup

* The file `.travis.yml` tells Travis-CI to install the requirements and then execute pytest.

```
dist: xenial
language: python
python: 3.7
install:
- pip install -r requirements.txt
- python setup.py install
script: pytest
```

* Other than configuring Travis-CI, no additional setup is required.  

## Continuous Deployment Setup

* Create an SSH key: `ssh-keygen -b 4096 -C 'build@travis-ci.com' -f ./deploy_rsa`
* Encrypt the private key: `travis encrypt-file deploy_rsa --pro --add`  This is use the travis-ci.com endpoint and 
add the appropriate line to the `.travis.yml` file.
* Edit the `.travis.yml` and change `before_install` to `before_deploy`.  The generated version makes the file 
available during testing, which isn't necessary - and is a security risk.
* Add `deploy_rsa.enc` and the edited version of `.travis.yml` to the repo.  **NOT** deploy_rsa, which is the 
unencrypted version!!!
* The following is the rest of `.travis.yml`.  Change the IP in `ssh_known_hosts` and `script`, and edit the 
path in `script` - both to match the server setup.

```
addons:
  ssh_known_hosts:
  - 3.16.42.52
before_deploy:
  - openssl aes-256-cbc -K $encrypted_f1cee75f37b0_key -iv $encrypted_f1cee75f37b0_iv -in deploy_rsa.enc -out deploy_rsa -d
  - chmod 600 deploy_rsa
deploy:
  provider: script
  skip_cleanup: true
  script: ssh -i deploy_rsa ubuntu@3.16.42.52 'source /home/ubuntu/ci-cd-repo/scripts/deploy.sh'
```
  