# Running in Kubernetes

This document provides a comprehensive guide to running in Kubernetes using Helm.

## Table of Contents

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Helm Chart](#helm-chart)
   - [chart.yaml](#chartyaml)
   - [values.yaml](#valuesyaml)
   - [templates/NOTES.txt](#templatesnotestxt)
4. [Deploying the Helm Chart](#deploying-the-helm-chart)
5. [Uninstalling the Helm Deployment](#uninstalling-the-helm-deployment)

## Introduction

This guide explains the setup and deployment process for the CFPB Helm Chart, which includes PostgreSQL, OpenSearch, and the CFGOV application. The Helm chart is configured to support local deployments.

## Requirements

1. **Local Kubernetes Cluster**:

   - Ensure you have a local Kubernetes cluster running. We only support [Docker Desktop](https://www.docker.com/products/docker-desktop) and [colima](https://github.com/abiosoft/colima).

2. **kubectl**:

   - Install `kubectl`, the Kubernetes command-line tool, by following the [official installation guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

3. **Helm**:

   - Install Helm, the package manager for Kubernetes, by following the [official installation guide](https://helm.sh/docs/intro/install/).

## Helm Chart

### chart.yaml

In our `chart.yaml` we bring two Helm chart dependencies:

- Opensearch
- Postgresql

### values.yaml

The `values.yaml` file contains our local configuration for the deployment of CFGOV.

#### Init Containers

We have two init containers:

1. Busybox:

   - Starts up once we have our Postgresql and Opensearch Pods running.
   - Serves as a pre-cursor to our cfgov-migrations container.

2. cfgov-migrations

   - Runs the django migrations and the `refresh-data.sh` script and populates it with test data `test.sql.gz`.
   - Indexes our database to Opensearch.

#### Containers

1. cfgov:

   - Uses the cfgov image, found in the repo's root `dockerfile`
   - Serves up our Django application on Port 8000 of the cfgov pod

2. cfgov-apache:

   - Built from `cfgov-apache` image built from the `apache/dockerfile`
   - Serves as a webserver to proxy to our cfgov container

### notes.txt

Our [notes.txt](https://helm.sh/docs/chart_template_guide/notes_files/) is split to work for local deployments and deployments to production.

```txt
{{- if .Values.localDeployment }}
{{ .Files.Get "notes/NOTES-local.txt" }}
{{- else }}
{{ .Files.Get "notes/NOTES-production.txt" }}
{{- end }}
```

## Deploying the CFGOV Helm Chart

Deploying the CFGOV Helm chart is simple with the `helm-init.sh` script.

To deploy the CFGOV Helm Chart you must:

1. make sure you have a the cfgov and cfgov-apache image built
2. have a local K8s cluster running (docker desktop, colima)

If these criteria are not met, the `helm-init.sh` script will not run.

## Viewing the Helm Chart

You can either user a K8s IDE ([lens](https://k8slens.dev/), [k9s](https://k9scli.io)) or manually portfward to view the application running.

Review the output of your deployment for more information on manually portforwarding.

| Pod        | Container    | Port             |
| ---------- | ------------ | ---------------- |
| cfgov      | cfgov        | 8000             |
| cfgov      | cfogv-apache | 80               |
| postgresql | postgresql   | 5432             |
| opensearch | opensearch   | 9200 (http)      |
|            |              | 9300 (transport) |
|            |              | 9600 (metrics)   |

## Uninstall the CFGOV Helm Chart

Running `helm-uninstall.sh` will uninstall the helm deploymennt of the CFGOV Helm Chart, as well as remove Persistent Volume Claims for the Open Search Pod and the Postgresql Pod.
