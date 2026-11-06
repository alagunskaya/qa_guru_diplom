pipeline {
    agent { label 'python' }

    // Добавляем таймстампы в консоль Jenkins
    options {
        timestamps()
    }

    parameters {
        string(name: 'SELENOID_LOGIN', description: 'Login for Selenoid')
        password(name: 'SELENOID_PASSWORD', description: 'Password for Selenoid')
        string(name: 'SELENOID_URL', description: 'URL for Selenoid')
    }

    stages {
        stage('Prepare Workspace') {
            steps {
                deleteDir()
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python -m venv .venv
                    source .venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Generate Environment Variables') {
            steps {
                // Создаем .env из безопасных параметров сборки
                writeFile file: '.env', text: """\
                    BASE_URL=https://fakestoreapi.com
                    SELENOID_LOGIN=${params.SELENOID_LOGIN}
                    SELENOID_PASSWORD=${params.SELENOID_PASSWORD}
                    SELENOID_URL=${params.SELENOID_URL}
                """.stripIndent()
            }
        }

        stage('Execute API Test Suite') {
            steps {
                sh '''
                    source .venv/bin/activate
                    python -m pytest tests/api --alluredir=allure-results
                '''
            }
        }

        stage('Execute UI Test Suite (Selenoid)') {
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
            // Генерация единого Allure-отчета
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}