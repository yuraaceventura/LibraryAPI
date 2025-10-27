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
                    sudo apt-get update
                    sudo apt-get install -y python3 python3-pip
                    pip install poetry
                    poetry config virtualenvs.create false
                    poetry install --only=main --no-root
                    '''
            }
        }

        stage('unit-test') {
            steps {
                sh "pip install -r requirements.txt"
                sh 'pytest --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
    }
}