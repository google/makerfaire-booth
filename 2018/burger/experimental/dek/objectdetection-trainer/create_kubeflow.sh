# Need Cloud Project w/ full owner access
# Need quota in region
# Get a GitHub API TOKEN:
# https://github.com/settings/tokens/new
export GITHUB_TOKEN=$(cat ~/github_token.txt)
export PATH=~/ks_0.10.2_linux_amd64:$PATH

#gcloud beta container --project seventh-oven-198801 clusters create cluster-1 --zone us-east1-c --username admin --cluster-version 1.10.2-gke.1 --machine-type n1-standard-8 --accelerator type=nvidia-tesla-p100,count=1 --image-type COS --disk-type pd-standard --disk-size 100 --scopes https://www.googleapis.com/auth/cloud-platform --num-nodes 3 --enable-cloud-logging --enable-cloud-monitoring --network default --subnetwork default --addons HorizontalPodAutoscaling,HttpLoadBalancing --enable-autorepair

#kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/stable/nvidia-driver-installer/cos/daemonset-preloaded.yaml

set -e


KUBEFLOW_VERSION=v0.1.2
KF_GKE_ENV=gke
KF_NAMESPACE=kubeflow

# kubectl create namespace ${KF_NAMESPACE}
# kubectl create clusterrolebinding default-admin --clusterrole=cluster-admin --user=dakoner@gmail.com

# rm -rf my-kubeflow
# ks init my-kubeflow

cd my-kubeflow
# ks registry add kubeflow github.com/kubeflow/kubeflow/tree/${KUBEFLOW_VERSION}/kubeflow
# ks pkg install kubeflow/core@${KUBEFLOW_VERSION}
# ks pkg install kubeflow/tf-serving@${KUBEFLOW_VERSION}
# ks pkg install kubeflow/tf-job@${KUBEFLOW_VERSION}

# ks generate core kubeflow-core --name=kubeflow-core

# ks param set kubeflow-core reportUsage true
# ks param set kubeflow-core usageId $(uuidgen)


# ks env add $KF_GKE_ENV
# ks param set kubeflow-core cloud gke --env=$KF_GKE_ENV
# ks param set kubeflow-core jupyterNotebookPVCMount /home/jovyan --env=$KF_GKE_ENV

# ks env set ${KF_GKE_ENV} --namespace ${KF_NAMESPACE}


# ks apply ${KF_GKE_ENV} -c kubeflow-core

JOB_NAME=myob

ks generate tf-job ${JOB_NAME} --name=${JOB_NAME}
ks apply ${KF_GKE_ENV} -c ${JOB_NAME}

# WArning: opens port to internet
# ks param set kubeflow-core jupyterHubServiceType LoadBalancer
# ks apply ${KF_GKE_ENV}

# Port forward just to local machine
#kubectl port-forward --namespace ${KF_NAMESPACE} $(kubectl get pod --namespace kubeflow --selector="app=tf-hub" -o jsonpath='{.items[0].metadata.name}') 8080:8000


				    

				 
