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
        IMAGE_ES7_REPO = 'cfpb/cfgov-elasticsearch-74'
        IMAGE_TAG = "${JOB_BASE_NAME}-${BUILD_NUMBER}"
        STACK_PREFIX = 'cfgov'
        NOTIFICATION_CHANNEL = 'cfgov-deployments'
        LAST_STAGE = 'Init'
        DEPLOY_SUCCESS = false
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
                    env.STACK_URL = dockerStack.getStackUrl(env.STACK_NAME)
                    env.CFGOV_HOSTNAME = dockerStack.getHostingDomain(env.STACK_NAME)
                    env.IMAGE_NAME_LOCAL = "${env.IMAGE_REPO}:${env.IMAGE_TAG}"
                    env.IMAGE_NAME_ES_LOCAL = "${env.IMAGE_ES_REPO}:${env.IMAGE_TAG}"
                    env.IMAGE_NAME_ES7_LOCAL = "${env.IMAGE_ES7_REPO}:${env.IMAGE_TAG}"
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
                    docker.build(env.IMAGE_NAME_ES7_LOCAL, '-f ./docker/elasticsearch/7.4/Dockerfile .')
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
                // scanImage(env.IMAGE_ES7_REPO, env.IMAGE_TAG) We Will Scan once Twistlock is configured to ignore known issues with this image.
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

                        image = docker.image(env.IMAGE_NAME_ES7_LOCAL)
                        image.push()
                        env.CFGOV_ES7_IMAGE = image.imageName()
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
                    DEPLOY_SUCCESS = true
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
                author = env.CHANGE_AUTHOR ? "by ${env.CHANGE_AUTHOR}" : "branch"
                changeUrl = env.CHANGE_URL ? env.CHANGE_URL : env.GIT_URL
                notify("${NOTIFICATION_CHANNEL}", 
                    """:white_check_mark: **${STACK_PREFIX} [${env.GIT_BRANCH}]($changeUrl)** $author [deployed](https://${env.CFGOV_HOSTNAME}/)! 
                    \n:jenkins: [Details](${env.RUN_DISPLAY_URL})    :mantelpiece_clock: [Pipeline History](${env.JOB_URL})    :docker-dance: [Stack URL](${env.STACK_URL}) """)
            }
        }

        unsuccessful {
            script{
                author = env.CHANGE_AUTHOR ? "by ${env.CHANGE_AUTHOR}" : "branch"
                changeUrl = env.CHANGE_URL ? env.CHANGE_URL : env.GIT_URL
                deployText = DEPLOY_SUCCESS ? "[deployed](https://${env.CFGOV_HOSTNAME}/) but failed" : "failed"
                notify("${NOTIFICATION_CHANNEL}", 
                    """:x: **${STACK_PREFIX} [${env.GIT_BRANCH}]($changeUrl)** $author $deployText at stage **${LAST_STAGE}** 
                    \n:jenkins-devil: [Details](${env.RUN_DISPLAY_URL})    :mantelpiece_clock: [Pipeline History](${env.JOB_URL})    :docker-dance: [Stack URL](${env.STACK_URL}) """)
            }
        }
    }
}
