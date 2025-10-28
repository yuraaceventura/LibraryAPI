pipeline {
    agent any
    
    stages {
        stage('git gheckout') {
            steps {
                checkout scm
            }
        }

        stage ("Installing dependencies") {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install poetry
                    poetry install --only=main --no-root
                    '''
            }
        }

        stage("Run APP") {
            steps {
                sh '''
                    docker-compose up -d
                '''
            }
        }
        stage('API-test') {
            steps {
                sh  '''
                    . .venv/bin/activate 
                    pytest --junitxml=test-results.xml
                    '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
    }
}