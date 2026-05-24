## Minikube commands to simulate a cluster
```
minikube start
```
```
minikube stop
```
```
minikube delete
```
Just running minikube with no arguments did not work for me, as my pods would not get up and running because of what seemed to be memory issues. To fix this i deleted my current minikube cluster with the above command and ran it with assigned memory, you can also assign cpu's i think:
```
minikube start --memory 7612
```

### Get external url for service (minikube only)
This command is what we use to get a url where we can access our application, in this case it is for user activity app so we can start and stop the simulation (remember that you have to be running your application in kubernetes before you can do this)
```
minikube service --url user-activity-app-service
minikube serbice --url grafana
```

## Running Kubernetes cluster, inspecting them, and deleting them
First ensure you have run 
```
minikube start
```
Then in the root folder of exercise 12, where all this readme file is located, and all our .yaml files are, run:
```
kubectl apply -f .
```
This applies all yaml files in the current directory. You can also call kubectl apply -f \<specific file> if you just want to apply one specific yaml file (maybe you have already deployed the all files but have made changes to one)


Then afterwards you can the following to get the status of all kubernetes services and such currently running.:
```
kubectl get all
```

To get logs of a pod, which we use to see the print statements of a given application, in this case the feedback collector since that is the one we have assigned to print the tuples it receives:
```
kubectl logs -f feedback-collector-69898db5dc-9dn9t
```

To delete all deployments, services, etc, run:
```
kubectl delete all --all
```

## Commands to build and push images
```bash
docker build -t noerklit/user_activity_app .
```
```bash
docker push noerklit/user_activity_app
```
```bash
docker build -t noerklit/recommender_app .
```
```bash
docker push noerklit/recommender_app
```
```bash
docker build -t noerklit/feedback_collector .
```
```bash
docker push noerklit/feedback_collector
```



