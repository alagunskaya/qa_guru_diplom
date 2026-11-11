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

        // Параметры для Telegram
        password(name: 'TELEGRAM_TOKEN', description: 'Telegram Bot Token')
        string(name: 'TELEGRAM_CHAT_ID', description: 'Telegram Chat ID')
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

            // Отправка уведомления в Telegram
            script {
                sh """
                    if [ ! -f "allure-report/widgets/summary.json" ]; then
                        echo "No Allure report found. Skipping Telegram notification."
                        exit 0
                    fi

                    JAR_VERSION=5.1.2
                    JAR="allure-notifications-\${JAR_VERSION}.jar"

                    if [ ! -f "\$JAR" ]; then
                        curl -fsSL -o "\$JAR" "https://github.com/qa-guru/allure-notifications/releases/download/v\${JAR_VERSION}/\$JAR" || \\
                        curl -fsSL -o "\$JAR" "https://github.com/qa-guru/allure-notifications/releases/download/\${JAR_VERSION}/\$JAR"
                    fi

                    # Передаем токен и чат через -D (системные свойства)
                    java -DconfigFile=notifications/telegram.json \\
                         "-Dnotifications.telegram.token=${params.TELEGRAM_TOKEN}" \\
                         "-Dnotifications.telegram.chat=${params.TELEGRAM_CHAT_ID}" \\
                         "-Dnotifications.base.reportLink=${env.BUILD_URL}allure/index.html" \\
                         "-Dnotifications.base.project=${env.JOB_BASE_NAME}" \\
                         -jar "\$JAR"
                """
            }
        }
    }
}