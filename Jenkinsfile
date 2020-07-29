// Jenkins multibranch pipeline geared towards building
// and deploying cf.gov production-like Docker stack.
//
// This pipeline uses Jenkins Shared Libraries for several
// pipeline steps. For details on how those work, see
// GHE repo: app-ops/app-ops-jenkins-shared-libraries
pipeline {
    agent {
        label 'docker-agent'
    }

    environment {
        IMAGE_REPO = 'cfpb/cfgov-python'
        IMAGE_TAG = "${JOB_BASE_NAME}-${BUILD_NUMBER}"
        STACK_PREFIX = 'cfgov'
        NOTIFICATION_CHANNEL = 'cfgov-deployments'
    }

    parameters {
        booleanParam(
            name: 'DEPLOY',
            defaultValue: true,
            description: 'Deploy the stack?'
        )
        booleanParam(
            name: 'REFRESH_DB',
            defaultValue: false,
            description: 'Refresh the database?'
        )
    }

    options {
        ansiColor('xterm')
        parallelsAlwaysFailFast()
        disableConcurrentBuilds()
        timestamps()
    }

    stages {
        stage('Init') {
            steps {
                script {
                    env.STACK_NAME = dockerStack.sanitizeStackName("${env.STACK_PREFIX}-${JOB_BASE_NAME}")
                    env.CFGOV_HOSTNAME = dockerStack.getHostingDomain(env.STACK_NAME)
                    env.IMAGE_NAME_LOCAL = "${env.IMAGE_REPO}:${env.IMAGE_TAG}"
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
            environment {
                DOCKER_BUILDKIT = '1'
            }
            steps {
                script {
                    docker.build(env.IMAGE_NAME_LOCAL, '--build-arg scl_python_version=rh-python36 --target cfgov-prod .')
                }
            }
        }

        stage('Scan Image') {
            steps {
                scanImage(env.IMAGE_REPO, env.IMAGE_TAG)
            }
        }

        stage('Push Image') {
            // Push image only on master branch or deploy is set to true
            when {
                anyOf {
                    branch 'master'
                    expression { return params.DEPLOY }
                }
            }
            steps {
                script {
                    docker.withRegistry(dockerRegistry.url, dockerRegistry.credentialsId) {
                        image = docker.image(env.IMAGE_NAME_LOCAL)
                        image.push()

                        // Sets fully-qualified image name
                        env.CFGOV_PYTHON_IMAGE = image.imageName()
                    }
                }
            }
        }

        stage('Deploy Stack') {
            // Deploys only on master branch or deploy is set to true
            when {
                anyOf {
                    branch 'master'
                    expression { return params.DEPLOY }
                }
            }
            steps {
                script {
                    timeout(time: 15, unit: 'MINUTES') {
                        dockerStack.deploy(env.STACK_NAME, 'docker-stack.yml')
                    }
                }
                echo "Site available at: https://${CFGOV_HOSTNAME}"
                notify("${NOTIFICATION_CHANNEL}", ":white_check_mark: PR ${env.CHANGE_URL} deployed by ${env.CHANGE_AUTHOR} via ${env.BUILD_URL} and available at https://${CFGOV_HOSTNAME}.")
            }
        }
        stage('Run Functional Tests') {
            when {
                anyOf {
                    branch 'master'
                    expression { return params.DEPLOY }
                }
            }
            steps {
                script {
                    timeout(time: 15, unit: 'MINUTES') {
                        // sh "docker-compose -f docker-compose.e2e.yml run e2e -e CYPRESS_baseUrl=https://${CFGOV_HOSTNAME}"
                        sh "docker run -v ${WORKSPACE}/test/cypress:/app/test/cypress -v ${WORKSPACE}/cypress.json:/app/cypress.json -w /app -e CYPRESS_baseUrl=https://${CFGOV_HOSTNAME} -e CI=1 cypress/included:4.10.0 npx cypress run -b chrome --headless"
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                if (env.GIT_BRANCH != 'master') {
                    notify("${NOTIFICATION_CHANNEL}", ":white_check_mark: Branch $env.GIT_BRANCH PR $env.CHANGE_URL deployed by $env.CHANGE_AUTHOR_EMAIL via $env.BUILD_URL and available at https://$env.CFGOV_HOSTNAME.")
                }
                else {
                    notify("${NOTIFICATION_CHANNEL}", ":white_check_mark: Branch $env.GIT_BRANCH deployed via $env.BUILD_URL and available at https://$env.CFGOV_HOSTNAME.")
                 }
            }
        }
        unsuccessful {
            notify("${NOTIFICATION_CHANNEL}", ":x: PR ${env.CHANGE_URL} by ${env.CHANGE_AUTHOR} failed. See: ${env.BUILD_URL}.")
        }
    }
}
