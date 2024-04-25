#! /usr/bin/bash

#docker build -t opendot . 
#docker run -it -d -p 8090:80 -v /home/ibrahim/sandbox/meryem/logs:/var/log/nginx:rw --name meryem meryem 
#docker run -it -d -p 8090:80 --restart always -v ./website:/www -v ~home/sandbox/opendot/logs:/var/log/nginx:rw --name opendot opendot 
#docker run -it meryem 
#docker run -it node
#docker exec -it meryem sh

#git add .
#git commit -am "$(date)"
#git push

# flask run

#python3 -m venv ./.venv/ --upgrade

docker image rm -f opendot
docker container rm -f opendot

docker buildx prune -f

. ./.venv/bin/activate

#pip install -r requirements.txt

#pip freeze > ./requirements.txt

docker build -t opendot .

docker run -it -d -p 8098:80 --restart always --name opendot opendot 

#python3 manage.py runserver 0.0.0.0:8000



# …or create a new repository on the command line
# echo "# opendot" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/skylinewebservice/opendot.git
# git push -u origin main
# …or push an existing repository from the command line
# git remote add origin https://github.com/skylinewebservice/opendot.git
# git branch -M main
# git push -u origin main