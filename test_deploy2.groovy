@Library('Dev Platforms Shared Libraries') _

pipeline{
    agent{
        kubernetes{
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
        stage('get docker version'){
            steps{
                script{
                    configureDocker()
                    docker --version
                }
            }
        }
    }
}