# tierchallenge

## Prerequisites:
    . AWS Credential to access a S3 Bucket
    . Ubuntu as lnx OS

## Installation steps :

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install unzip jq git conntrack -y
```

> Install kubectl

```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo cp ./kubectl /usr/local/bin
export PATH=/usr/local/bin:$PATH
kubectl version
```

> Install aws cli

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

> Install Docker

```bash
wget -qO- https://get.docker.com/ | sh
sudo usermod -aG docker $(whoami)
#log out & log in again to update user profile
docker version
docker info
````

> Install minikube

```bash
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube
sudo cp ./minikube /usr/local/bin
minikube version

sudo -i

# Start Minikube
minikube start --vm-driver=none

# enable ingress controller
sudo minikube addons enable ingress
````


> Clone repository and update yaml files

```bash
git clone https://github.com/gclntm/tierchallenge.git


cd tierchallenge

#Update secrets with AWS access key
sed -i 's/{{aws_access_key_id}}/'"$(echo -n 'YOUR_ACCESS_KEY_ID' | base64)"'/g' k8s/secrets.yaml
sed -i 's/{{aws_secret_access_key}}/'"$(echo -n 'YOUR_ACCESS_SECRET_KEY' | base64)"'/g' k8s/secrets.yaml
sed -i 's/{{aws_default_region}}/'"$(echo -n 'YOUR_DEFAULT_REGION' | base64)"'/g' k8s/secrets.yaml

#Get local IP to update minikube external IP
EXTERNAL_IP=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)
sed -i 's/{{EXTERNAL_IP}}/'"$EXTERNAL_IP"'/g' k8s/deployment.yaml
tail -4 k8s/deployment.yaml

#Create a dedicated namespace
sudo kubectl create -f k8s/namespace.yaml
#Change namespace context
sudo kubectl config set-context --current --namespace tierchallenge
#Deploy secrets, app, service & ingress
sudo kubectl create -f k8s/secrets.yaml
sudo kubectl create -f k8s/deployment.yaml
sudo kubectl create -f k8s/secrets.yaml
sudo kubectl create -f k8s/ingress.yaml


#Wait for deployment to complete (ctrl-c to exit)
sudo kubectl get pods -w

#Confirm external ip exposure
sudo kubectl get service

#Get POD name
POD_NAME=`sudo kubectl get pods -o jsonpath='{.items[0].metadata.name}'`

#Confirm flask app is running
sudo kubectl logs pod/$POD_NAME

#Open a shell inside the pod
sudo kubectl exec -it $POD_NAME -- /bin/bash
#Confirm ENV variables
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
echo $AWS_DEFAULT_REGION


#Get internal cluster IP
FRONTEND_SERVICE_IP=`sudo kubectl get service/objects-api -o jsonpath='{.spec.clusterIP}'`
echo $FRONTEND_SERVICE_IP

#Test internal access
curl -i http://$FRONTEND_SERVICE_IP/v1/listobjects_html
curl -i http://$FRONTEND_SERVICE_IP/v1/listobjects_json


#Test external access
echo http://$(curl http://169.254.169.254/latest/meta-data/public-hostname)/v1/listobjects_html
echo http://$(curl http://169.254.169.254/latest/meta-data/public-hostname)/v1/listobjects_json

Copy paste to browser

````

> Done.
