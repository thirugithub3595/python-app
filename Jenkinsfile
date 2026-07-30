pipeline {
    agent any

    environment {
        IMAGE_NAME = 'thiruvenkadam/python-app'
        IMAGE_TAG = 'v1'
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Verify Image') {
            steps {
                sh 'docker images | grep python-app'
            }
        }
    }

    post {
        success {
            echo 'Docker image built successfully'
        }
        failure {
            echo 'Docker build failed'
        }
    }
}
