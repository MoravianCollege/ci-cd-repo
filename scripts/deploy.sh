sudo systemctl stop cicd
cd /home/ubuntu/ci-cd-repo/ && git pull origin master
sudo systemctl start cicd
