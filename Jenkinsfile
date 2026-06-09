pipeline {
    agent any

    environment {
        PYTHON_PATH = 'python3'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Instalar dependencias') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r tests/requirements-test.txt
                '''
            }
        }

        stage('Pruebas automatizadas') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest tests/test_api.py -v --junitxml=reports/test-results.xml
                '''
            }
            post {
                always {
                    junit 'reports/test-results.xml'
                }
            }
        }

        stage('Build Docker image') {
            steps {
                sh 'docker build -t moncada-gold-inventory:${BUILD_NUMBER} ./app'
            }
        }

        stage('Verificar contenedores') {
            steps {
                sh '''
                    docker-compose up -d --build
                    sleep 20
                    curl -f http://localhost:5000/health || exit 1
                    docker-compose down
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline Moncada Gold completado exitosamente.'
        }
        failure {
            echo 'Pipeline fallido. Revisar logs para detalles.'
        }
        always {
            cleanWs()
        }
    }
}
