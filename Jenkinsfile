pipeline {
    agent { 
        dockerContainer { 
            image 'python:3.9-slim' 
        } 
    }
    
    stages {
        stage('git gheckout') {
            steps {
                checkout scm
            }
        }

        stage ("Installing dependencies") {
            steps {
                sh '''
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