pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'git@github.com:thirugithub3595/python-app.git'
            }
        }

        stage('Build') {
            steps {
                sh 'echo Building Flask project'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Success') {
            steps {
                echo 'Pipeline executed successfully'
            }
        }
    }
}
