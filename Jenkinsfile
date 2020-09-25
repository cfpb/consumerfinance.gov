// Jenkins multibranch pipeline geared towards building
// and deploying cf.gov production-like Docker stack.
//
// This pipeline uses Jenkins Shared Libraries for several
// pipeline steps. For details on how those work, see
// GHE repo: app-ops/app-ops-jenkins-shared-libraries
pipeline {
    agent {
        label 'docker'
    }

    environment {
        IMAGE_REPO = 'cfpb/cfgov-python'
        IMAGE_ES_REPO = 'cfpb/cfgov-elasticsearch-23'
        IMAGE_TAG = "${JOB_BASE_NAME}-${BUILD_NUMBER}"
        STACK_PREFIX = 'cfgov'
        NOTIFICATION_CHANNEL = 'cfgov-deployments'
        LAST_STAGE = 'Init'
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
                    env.IMAGE_NAME_ES_LOCAL = "${env.IMAGE_ES_REPO}:${env.IMAGE_TAG}"
                }
                sh 'env | sort'
            }
        }

        stage('Checkout') {
            steps {
                dir('static.in/cfgov-fonts') {
                    script {
                        LAST_STAGE = env.STAGE_NAME
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
                    LAST_STAGE = env.STAGE_NAME
                    docker.build(env.IMAGE_NAME_LOCAL, '--build-arg scl_python_version=rh-python36 --target cfgov-prod .')
                    docker.build(env.IMAGE_NAME_ES_LOCAL, '-f ./docker/elasticsearch/Dockerfile .')
                }
            }
        }

        stage('Scan Image') {
            steps {
                script {
                    LAST_STAGE = env.STAGE_NAME
                }
                scanImage(env.IMAGE_REPO, env.IMAGE_TAG)
                scanImage(env.IMAGE_ES_REPO, env.IMAGE_TAG)
            }
        }

        stage('Push Image') {
            // Push image only on main branch or deploy is set to true
            when {
                anyOf {
                    branch 'main'
                    expression { return params.DEPLOY }
                }
            }
            steps {
                script {
                    LAST_STAGE = env.STAGE_NAME
                    docker.withRegistry(dockerRegistry.url, dockerRegistry.credentialsId) {
                        image = docker.image(env.IMAGE_NAME_LOCAL)
                        image.push()

                        // Sets fully-qualified image name
                        env.CFGOV_PYTHON_IMAGE = image.imageName()

                        image = docker.image(env.IMAGE_NAME_ES_LOCAL)
                        image.push()
                        env.CFGOV_ES_IMAGE = image.imageName()
                    }
                }
            }
        }

        stage('Deploy Stack') {
            // Deploys only on main branch or deploy is set to true
            when {
                anyOf {
                    branch 'main'
                    expression { return params.DEPLOY }
                }
            }
            steps {
                script {
                    LAST_STAGE = env.STAGE_NAME
                    timeout(time: 30, unit: 'MINUTES') {
                        dockerStack.deploy(env.STACK_NAME, 'docker-stack.yml')
                    }
                }
                echo "Site available at: https://${CFGOV_HOSTNAME}"
            }
        }

        stage('Run Functional Tests') {
            when {
                anyOf {
                    branch 'main'
                    expression { return params.DEPLOY }
                }
            }
            steps {
                script {
                    LAST_STAGE = env.STAGE_NAME
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
                if (env.GIT_BRANCH != 'main') {
                    notify("${NOTIFICATION_CHANNEL}", ":white_check_mark: [**${env.GIT_BRANCH}**](${env.CHANGE_URL}) by ${env.CHANGE_AUTHOR} deployed via [Jenkins](${env.BUILD_URL}) and available at https://${env.CFGOV_HOSTNAME}/")
                }
                else {
                    notify("${NOTIFICATION_CHANNEL}", ":white_check_mark: **main** branch stack deployed via [Jenkins](${env.BUILD_URL}) and available at https://${env.CFGOV_HOSTNAME}/")
                }
            }
        }
        unsuccessful {
            script{
                if (env.GIT_BRANCH != 'main') {
                    notify("${NOTIFICATION_CHANNEL}", ":x: [**${env.GIT_BRANCH}**](${env.CHANGE_URL}) by ${env.CHANGE_AUTHOR} failed at stage **${LAST_STAGE}** \n:jenkins-devil: [Failure Details](${env.RUN_DISPLAY_URL})    :mantelpiece_clock: [Pipeline History](${env.JOB_URL})")
                }
                else {
                    notify("${NOTIFICATION_CHANNEL}", ":x: **main** branch stack deployment failed at stage **${LAST_STAGE}** \n:jenkins-devil: [Failure Details](${env.RUN_DISPLAY_URL})    :mantelpiece_clock: [Pipeline History](${env.JOB_URL})")
                }
            }
        }
    }
}
