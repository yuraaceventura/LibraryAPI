pipeline {
    agent {
        docker {
            image 'python:slim' // Or any other suitable Python image
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
                sh "pip install poetry"
                sh "poetry config virtualenvs.create false"
                sh "poetry install --only=main --no-root"
            }
        }

        stage('unit-test') {
            steps {
                sh "pip install -r requirements.txt"
                sh 'pytest ./tests'
            }
        }
    }
}