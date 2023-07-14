@Library('Dev Platforms Shared Libraries') _

pipeline{
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
'''
    }
  }

    stages{
        stage('Build Images') {
            steps {
                script {
                configureDocker()
                sh '''
                echo "$secret"
                echo $secret
                echo $DOCKER_HOST_IP

                echo "this is the IP"
                curl ipconfig.me
                '''
                }
            }
        }
    }
}
