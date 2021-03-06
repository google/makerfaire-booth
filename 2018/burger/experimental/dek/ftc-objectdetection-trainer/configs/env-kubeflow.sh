#!/bin/bash
#
# Script that defines various environment variables.
# This is script defines values for all the variables used in
# the instructions.

# Bucket and project must be unique for each project

# Set PROJECT to the project you want to use with Kubeflow.
export PROJECT=ftc-research

# Set DEPLOYMENT_NAME to the name to give to the deployment.
# The name must be unique for each deployment within your project.
export DEPLOYMENT_NAME=ftc-cluster

# Set this to the zone in your ${CONFIG_FILE}
export ZONE=us-west1-a

# Set config file to the YAML file defining your deployment manager configs.
export CONFIG_FILE=cluster-${PROJECT}.yaml

# Get the project number
export PROJECT_NUMBER=`gcloud projects describe ${PROJECT} --format='value(project_number)'`
