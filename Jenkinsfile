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

        stage('unit-test') {
            steps {
                sh  '''
                    . /var/jenkins_home/workspace/my_pipe_master/.venv/bin/activate
                    pip install -r requirements.txt
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