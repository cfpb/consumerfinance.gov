node {
    stage('Unit Testing') {
        parallel(
            'Front-end tests': {
                def node = tool name: 'Node 8x Current', type: 'jenkins.plugins.nodejs.tools.NodeJSInstallation'
                env.PATH = '${node}/bin:${env.PATH}'
                sh './run_travis.sh frontend'
            },
            'Back-end tests': {
                sh './run_travis.sh backend'
            },
            'Acceptance tests': {
                def node = tool name: 'Node 8x Current', type: 'jenkins.plugins.nodejs.tools.NodeJSInstallation'
                env.PATH = '${node}/bin:${env.PATH}'
                sh './run_travis.sh acceptance'
            }
        )
    }
    stage('Coverage') {
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
