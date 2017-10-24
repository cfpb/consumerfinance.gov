pipeline {
    agent any
    options {
        timeout(time: 1, unit: 'HOURS') 
        tool name: 'Node 8x Current', type: 'jenkins.plugins.nodejs.tools.NodeJSInstallation'
    }
    triggers {
        pollSCM('* * * * *')
    }
    stages {
        stage('Unit Testing') {
            steps {
                parallel(
                    "Front-End Tests": {
                        sh './run_travis.sh frontend'
                    },
                    "Back-End Tests": {
                        sh './run_travis.sh backend'
                    },
                    "Acceptance Tests": {
                        sh './run_travis.sh acceptance'
                    }
                )
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
