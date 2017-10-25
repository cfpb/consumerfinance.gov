pipeline {
    agent any
    options {
        timeout(time: 1, unit: 'HOURS') 
        timestamps()
    }
    tools {
        jenkins.plugins.nodejs.tools.NodeJSInstallation 'Node 8x Current'
    }
    triggers {
        pollSCM('* * * * *')
    }
    stages {
        stage('Unit Testing') {
            steps {
                parallel {
                    stage('Front-end tests') {
                        steps {
                            sh './run_travis.sh frontend'
                        },
                    }
                    stage('Back-end tests") {
                        steps {
                            sh './run_travis.sh backend'
                        }
                    }
                    stage('Acceptance tests') {
                        steps {
                            sh './run_travis.sh acceptance'
                        }
                    }
                }
            }
        }
        stage('Coverage') {
            steps {
                parallel(
                    "Front-End Coverage": {
                        sleep 1
                        echo 'Hello front-end coverage!'
                    },
                    "Back-End Coverage": {
                        sleep 1
                        echo 'Hello back-end coverage!'
                    }
                )
            }
        }
    }
}
