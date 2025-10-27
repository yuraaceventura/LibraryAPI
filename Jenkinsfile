pipeline {
    agent any

    stages {
        stage('git gheckout') {
            steps {
                checkout scm
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