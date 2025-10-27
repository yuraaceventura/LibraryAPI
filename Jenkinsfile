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
                sh 'pytest ./tests'
            }
        }
    }
}