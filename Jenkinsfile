pipeline {

    agent {
        label 'docker-agent'
    }

    environment {
        IMAGE_REPO="${DOCKER_REGISTRY}/cfpb/cfgov-python"
        IMAGE_TAG="${JOB_BASE_NAME}-${BUILD_NUMBER}"
        SCAN_IMAGE = 'true'
        STACK_PREFIX = 'cfgov'
    }

    parameters {
        string(
            name: 'ENV_NAME',
            defaultValue: env.JOB_BASE_NAME,
            description: 'Environment name'
        )

        booleanParam(
            name: 'DEPLOY', 
            defaultValue: false,
            description: 'Deploy the stack?'
        )
    }

    options {
        ansiColor('xterm')
        parallelsAlwaysFailFast()
        timestamps()
    }
    
    stages {

        stage ('Init') {
            steps {
                script {
                    env.STACK_NAME = stack.scrubStackName(params.ENV_NAME)
                    env.CFGOV_HOSTNAME = stack.getWebHostDomain(env.STACK_NAME)
                    env.IMAGE_NAME = "${IMAGE_REPO}:${IMAGE_TAG}"
                }
                sh 'env | sort'
            }
        }

        stage('Checkout') {
            steps {
                dir('static.in/cfgov-fonts') {
                    script {
                        git ghe.getRepoUrl('CFGOV/cfgov-fonts')
                    }
                }
            }
        }

        stage('Build Image') {
            steps {
                script {
                    docker.build(env.IMAGE_NAME, "--build-arg scl_python_version=rh-python36 --target cfgov-prod .")
                }
            }
        }

        stage('Scan Image') {
            when {
                environment name: 'SCAN_IMAGE', value: 'true' 
            }
            steps {
                scanImage(env.IMAGE_REPO, env.IMAGE_TAG)
            }
        }

        stage('Push Image') {
            when {
                expression { return params.DEPLOY }
            } 
            steps {
                script {
                    docker.withRegistry(env.DOCKER_REGISTRY_URL, env.DOCKER_REGISTRY_CREDENTIALS_ID) {
                        docker.image(env.IMAGE_NAME).push()
                    }
                }
            }
        }

        stage('Deploy Stack') {
            when {
                expression { return params.DEPLOY }
            } 
            options {
                timeout(time: 15, unit: 'MINUTES')
            }
            steps {
                deployStack(env.STACK_NAME, 'docker-stack.yml')
                echo "Site available at: https://${CFGOV_HOSTNAME}"
            }
            post {
                unsuccessful {
                    echo "Stack '${STACK_NAME}' failed to deploy."
                    //FIXME: Implement this.
                    //showStack(env.STACK_NAME)
                }
            }
        }
    }
}