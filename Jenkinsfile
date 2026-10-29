pipeline {
    // Запускаем только на агентах с меткой python
    agent { label 'python' }

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

        stage('Install and Run Tests') {
            steps {
                sh '''
                    python -m venv .venv
                    source .venv/bin/activate
                    pip install -r requirements.txt
                    pytest tests/ --alluredir=allure-results
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