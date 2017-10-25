pipeline {
    agent any
    options {
        timeout(time: 1, unit: 'HOURS') 
        timestamps()
    }
    triggers {
        pollSCM('* * * * *')
    }
    stages {
        stage('Unit Testing') {
            steps {
                // Abort any still-running stages if one fails
                failFast true
                parallel {
                    stage('Front-end tests') {
                        def node = tool name: 'Node 8x Current', type: 'jenkins.plugins.nodejs.tools.NodeJSInstallation'
                        env.PATH = "${node}/bin:${env.PATH}"
                        steps {
                            sh './run_travis.sh frontend'
                        }
                    }
                    stage('Back-end tests') {
                        steps {
                            sh './run_travis.sh backend'
                        }
                    }
                    stage('Acceptance tests') {
                        def node = tool name: 'Node 8x Current', type: 'jenkins.plugins.nodejs.tools.NodeJSInstallation'
                        env.PATH = "${node}/bin:${env.PATH}"
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
