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
                    'Front-end tests': {
                        script {
                            def node = tool name: 'Node 8x Current', type: 'jenkins.plugins.nodejs.tools.NodeJSInstallation'
                            env.PATH = '${node}/bin:${env.PATH}'
                            sh './run_travis.sh frontend'
                        }
                    },
                    'Back-end tests': {
                        sh './run_travis.sh backend'
                    },
                    'Acceptance tests': {
                        script {
                            def node = tool name: 'Node 8x Current', type: 'jenkins.plugins.nodejs.tools.NodeJSInstallation'
                            env.PATH = '${node}/bin:${env.PATH}'
                            sh './run_travis.sh acceptance'
                        }
                    }
                )
            }
        }
        stage('Coverage') {
            steps {
                parallel(
                    'Front-End Coverage': {
                        sleep 1
                        echo 'Hello front-end coverage!'
                    },
                    'Back-End Coverage': {
                        sleep 1
                        echo 'Hello back-end coverage!'
                    }
                )
            }
        }
    }
}
