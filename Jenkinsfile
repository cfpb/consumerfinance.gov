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
                parallel(
                    "Front-End Tests": {
                        sh '''
                        echo $PATH
                        export PATH=/var/lib/jenkins/tools/jenkins.plugins.nodejs.tools.NodeJSInstallation/Node_8x_Current/bin:/var/lib/jenkins/tools/jenkins.plugins.nodejs.tools.NodeJSInstallation/Node_8x_Current/node_modules:$PATH
                        echo $PATH
                        node --version
                        ./run_travis.sh frontend
                        '''
                    },
                    "Back-End Tests": {
                        sh './run_travis.sh backend'
                    },
                    "Acceptance Tests": {
                        sh '''
                        echo $PATH
                        export PATH=/var/lib/jenkins/tools/jenkins.plugins.nodejs.tools.NodeJSInstallation/Node_8x_Current/bin:/var/lib/jenkins/tools/jenkins.plugins.nodejs.tools.NodeJSInstallation/Node_8x_Current/node_modules:$PATH
                        echo $PATH
                        node --version
                        ./run_travis.sh acceptance
                        '''
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
