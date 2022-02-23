// Jenkins multibranch pipeline geared towards building
// and deploying cf.gov production-like Docker stack.
//
// This pipeline uses Jenkins Shared Libraries for several
// pipeline steps. For details on how those work, see
// GHE repo: app-ops/app-ops-jenkins-shared-libraries

def postGitHubStatus(String context, String status, String message, String url) {
    masked_url = url.replace(env.JENKINS_URL, "http://dev-jenkins/")
    withCredentials([string(credentialsId: 'cfpbot-github-api-token', variable: 'GITHUB_TOKEN')]) {
        sh "curl https://api.github.com/repos/cfpb/consumerfinance.gov/statuses/\${GIT_COMMIT} -H \"Authorization: token \${GITHUB_TOKEN}\" -H 'Content-Type: application/json' -X POST -d '{\"state\": \"$status\", \"context\": \"$context\", \"description\": \"$message\", \"target_url\": \"$masked_url\"}'"
    }
}

pipeline {
    agent {
        label 'docker'
    }

    environment {
        IMAGE_REPO = 'cfpb/cfgov-python'
        IMAGE_ES_REPO = 'cfpb/cfgov-elasticsearch'
        // Elasticsearch image tag should be the same as that defined in Dockerfile
        IMAGE_ES_TAG = '7.16.2'
        // Only Python image tag changes for every build
        PYTHON_IMAGE_TAG = "${JOB_BASE_NAME}-${BUILD_NUMBER}"
        STACK_PREFIX = 'cfgov'
        NOTIFICATION_CHANNEL = 'cfgov-deployments'
        LAST_STAGE = 'Init'
        DEPLOY_SUCCESS = false
        // Determines if Elasticsearch image should be updated
        IS_ES_IMAGE_UPDATED = 'false'
        DOCKER_HUB_REGISTRY = 'https://registry.hub.docker.com'
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
                    env.IMAGE_NAME_LOCAL = "${env.IMAGE_REPO}:${env.PYTHON_IMAGE_TAG}"
                    env.IMAGE_NAME_ES_LOCAL = "${env.IMAGE_ES_REPO}:${env.IMAGE_ES_TAG}"
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
                script {
                    env.GIT_COMMIT = sh(
                        returnStdout: true,
                        script: "git rev-parse HEAD | cut -c1-7"
                    ).trim()
                }
            }
        }

        stage('Check Image') {
            environment {
                DTR_REGISTRY = 'https://dtr-registry.cfpb.gov'
            }
            when { expression { env.BRANCH_NAME != 'main' } }
            steps {
                script {
                    sh "git config --add remote.origin.fetch +refs/heads/main:refs/remotes/origin/main"
                    sh "git fetch --no-tags"

                    List<String> sourceChanged = sh(
                        returnStdout: true,
                        script: "git diff --name-only origin/main..origin/${env.BRANCH_NAME}"
                    ).split()

                    for (int i = 0; i < sourceChanged.size(); i++) {
                        if (sourceChanged[i].contains("docker/elasticsearch/Dockerfile")) {
                            IS_ES_IMAGE_UPDATED = 'true'
                        }
                    }

                    // get token to be able to list image tags in Docker Hub
                    // https://hub.docker.com/support/doc/how-do-i-authenticate-with-the-v2-api
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'docker-hub-cfpb',
                            passwordVariable: 'DOCKER_HUB_PASSWORD',
                            usernameVariable: 'DOCKER_HUB_USER'
                        )
                    ]) {
                        sh 'docker login $DOCKER_HUB_REGISTRY -u $DOCKER_HUB_USER -p $DOCKER_HUB_PASSWORD'
                        String dockerToken = sh(
                            returnStdout: true,
                            script: 'curl -s -H "Content-Type: application/json" -X POST -d \'{"username": "\'$DOCKER_HUB_USER\'", "password": "\'$DOCKER_HUB_PASSWORD\'"}\' $DOCKER_HUB_REGISTRY/v2/users/login/ | jq -r .token'
                        )
                        List<String> elasticsearchTags = sh(
                            returnStdout: true,
                            script: 'curl -s -H "Authorization: JWT $dockerToken" $DOCKER_HUB_REGISTRY/v2/repositories/$IMAGE_ES_REPO/tags | jq -r \'.results|.[]|.name\''
                        ).split()
                        for (int i = 0; i < elasticsearchTags.size(); i++) {
                            if (elasticsearchTags[i].contains("${env.IMAGE_ES_TAG}")) {
                                IS_ES_IMAGE_UPDATED = 'false'
                            }
                        }
                        echo "ES image is updated: ${IS_ES_IMAGE_UPDATED}"
                    }

                    withCredentials([
                        usernamePassword(
                            credentialsId: 'dtr-ext-jenkins-service',
                            passwordVariable: 'DOCKER_HUB_PASSWORD',
                            usernameVariable: 'DOCKER_HUB_USER'
                        )
                    ]) {
                        sh 'docker login $DTR_REGISTRY -u $DOCKER_HUB_USER -p $DOCKER_HUB_PASSWORD'
                        String dockerToken = sh(
                            returnStdout: true,
                            script: 'curl -s -H "Content-Type: application/json" -X POST -d \'{"username": "\'$DOCKER_HUB_USER\'", "password": "\'$DOCKER_HUB_PASSWORD\'"}\' $DTR_REGISTRY/v2/users/login/'
                        )
                        List<String> elasticsearchTags = sh(
                            returnStdout: true,
                            script: 'curl -s -H "Authorization:Bearer $dockerToken" $DTR_REGISTRY/v2/$IMAGE_ES_REPO/tags/list | jq \'.tags[:10]\''
                        ).split()
                    }
                }
            }
        }

        stage('Build Image') {
            environment {
                DOCKER_BUILDKIT = '0'
                COMPOSE_DOCKER_CLI_BUILD = '0'
            }
            steps {
                postGitHubStatus("jenkins/deploy", "pending", "Building", env.RUN_DISPLAY_URL)

                script {
                    LAST_STAGE = env.STAGE_NAME

                    docker.withRegistry(dockerRegistry.url, dockerRegistry.credentialsId) {
                        docker.build(
                            env.IMAGE_NAME_LOCAL,
                            '--target cfgov-prod .'
                        )
                        if (IS_ES_IMAGE_UPDATED == 'true') {
                            echo "Building ES image"
                            docker.build(
                                env.IMAGE_NAME_ES_LOCAL,
                                '-f ./docker/elasticsearch/Dockerfile .'
                            )
                        }
                    }
                }
            }
        }

        stage('Scan Image') {
            steps {
                postGitHubStatus("jenkins/deploy", "pending", "Scanning", env.RUN_DISPLAY_URL)

                script {
                    LAST_STAGE = env.STAGE_NAME
                    scanImage(env.IMAGE_REPO, env.PYTHON_IMAGE_TAG)
                    if (IS_ES_IMAGE_UPDATED == 'true') {
                        echo "Scanning ES image"
                        scanImage(env.IMAGE_ES_REPO, env.IMAGE_ES_TAG)
                    }
                }
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
                    }
                    docker.withRegistry("${DOCKER_HUB_REGISTRY}", 'docker-hub-cfpb') {
                        image = docker.image(env.IMAGE_NAME_ES_LOCAL)
                        if (IS_ES_IMAGE_UPDATED == 'true') {
                            echo "Pushing ES image"
                            image.push()
                        }
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
                postGitHubStatus("jenkins/deploy", "pending", "Deploying", env.RUN_DISPLAY_URL)
                script {
                    LAST_STAGE = env.STAGE_NAME
                    timeout(time: 30, unit: 'MINUTES') {
                        dockerStack.deploy(env.STACK_NAME, 'docker-stack.yml')
                    }
                    DEPLOY_SUCCESS = true
                }

                echo "Site available at: https://${CFGOV_HOSTNAME}"

                postGitHubStatus("jenkins/deploy", "success", "Deployed", env.RUN_DISPLAY_URL)
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

                if (env.DEPLOY_SUCCESS == false) {
                    postGitHubStatus("jenkins/deploy", "failure", "Failed", env.RUN_DISPLAY_URL)
                    postGitHubStatus("jenkins/functional-tests", "error", "Cancelled", env.RUN_DISPLAY_URL)
                    deployText = "failed"
                } else {
                    postGitHubStatus("jenkins/functional-tests", "failure", "Failed", env.RUN_DISPLAY_URL)
                    deployText = "[deployed](https://${env.CFGOV_HOSTNAME}/) but failed"
                }

                notify("${NOTIFICATION_CHANNEL}",
                    """:x: **${STACK_PREFIX} [${env.GIT_BRANCH}]($changeUrl)** $author $deployText at stage **${LAST_STAGE}**
                    \n:jenkins-devil: [Details](${env.RUN_DISPLAY_URL})    :mantelpiece_clock: [Pipeline History](${env.JOB_URL})    :docker-dance: [Stack URL](${env.STACK_URL}) """)

            }
        }
    }
}
