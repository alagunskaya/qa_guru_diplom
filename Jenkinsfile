pipeline {
    agent { label 'python' }

    parameters {
        string(name: 'SELENOID_LOGIN', description: 'Login for Selenoid')
        password(name: 'SELENOID_PASSWORD', description: 'Password for Selenoid')
        string(name: 'SELENOID_URL', description: 'URL for Selenoid')
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m venv .venv
                    source .venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Create .env file') {
            steps {
                writeFile file: '.env', text: """\
                    BASE_URL=https://fakestoreapi.com
                    SELENOID_LOGIN=${params.SELENOID_LOGIN}
                    SELENOID_PASSWORD=${params.SELENOID_PASSWORD}
                    SELENOID_URL=${params.SELENOID_URL}
                """.stripIndent()
            }
        }

        stage('Run API Tests') {
            steps {
                sh '''
                    source .venv/bin/activate
                    python -m pytest tests/api --alluredir=allure-results
                '''
            }
        }

        stage('Run UI Tests') {
            steps {
                sh '''
                    source .venv/bin/activate
                    python -m pytest tests/ui --alluredir=allure-results --selenoid
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}