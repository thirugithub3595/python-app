pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                sh 'echo Building Flask application'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 --version'
                sh 'echo Running tests'
            }
        }

        stage('Success') {
            steps {
                echo 'Pipeline executed successfully'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }

        success {
            echo 'Build succeeded'
        }

        failure {
            echo 'Build failed'
        }
    }
}
