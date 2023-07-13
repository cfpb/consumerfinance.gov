@Library('Dev Platforms Shared Libraries') _

pipeline {
  agent {
    kubernetes {
      defaultContainer 'python'
      yaml '''
kind: Pod
spec:
  serviceAccountName: cfpb-ci-sa
  containers:
  - name: python
    image: python:3-alpine
    imagePullPolicy: Always
    command:
    - cat
    tty: true
  - name: helm
    image: alpine/helm:latest
    imagePullPolicy: Always
    command:
    - cat
    tty: true
'''
    }
  }

  environment {
    DOCKER_REGISTRY_REPO = 'cfpb/appops'
    AWS_REGION = 'us-east-1'
  }

  options {
    ansiColor('xterm')
    disableConcurrentBuilds()
  }
  

  stages {
    stage('Install Dependencies') {
      steps {
        script {
          env.AWS_ACCOUNT_ID = "795649122172"
          env.DOCKER_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
          env.DOCKER_IMAGE = "${DOCKER_REGISTRY}/${DOCKER_REGISTRY_REPO}/cfgov:latest"
        }
      }
    }

    stage('Build Images') {
      steps {
        script {
          configureDocker()
          echo "Building $DOCKER_IMAGE"
          docker.build("${DOCKER_IMAGE}", "--pull -f Dockerfile .")
        }
      }
    }

    stage('Push Scanned Images') {
      steps {
        script {
          sh '''
          apk add aws-cli > /dev/null
          aws ecr get-login-password | docker login --username AWS --password-stdin "$DOCKER_REGISTRY"
          '''
          docker.image("${DOCKER_IMAGE}").push()
        }
      }
    }

    
  }
}