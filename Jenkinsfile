pipeline {
agent any

environment {
    IMAGE_NAME = 'thiruvenkadam/python-app'
    IMAGE_TAG = "${BUILD_NUMBER}"
}

stages {

    stage('Checkout') {
        steps {
            checkout scm
        }
    }

    stage('Verify environment') {
        steps {
            sh 'git --version'
            sh 'docker --version'
            sh 'python3 --version'
        }
    }

    stage('Build Docker image') {
        steps {
            sh '''
            docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
            '''
        }
    }

    stage('Verify Docker image') {
        steps {
            sh 'docker images | grep python-app'
        }
    }

    stage('Trivy scan') {
        steps {
            sh '''
            if command -v trivy >/dev/null; then
                trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:${IMAGE_TAG}
            else
                echo "Trivy not installed, skipping scan"
            fi
            '''
        }
    }

    stage('Docker Hub login') {
        steps {
            withCredentials([usernamePassword(
                credentialsId: 'dockerhub-creds',
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASS'
            )]) {
                sh '''
                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                '''
            }
        }
    }

    stage('Push Docker image') {
        steps {
            sh '''
            docker push ${IMAGE_NAME}:${IMAGE_TAG}
            docker push ${IMAGE_NAME}:latest
            '''
        }
    }

    stage('Deploy') {
        steps {
            sh '''
            docker compose down || true
            docker compose up --build -d
            '''
        }
    }

    stage('Health check') {
        steps {
            sh '''
            for i in {1..10}; do
                if curl -f http://localhost:5000; then
                    echo "Application is healthy"
                    exit 0
                fi
                echo "Waiting for application..."
                sleep 3
            done
            echo "Health check failed"
            exit 1
            '''
        }
    }
}

post {
    always {
        sh 'docker logout || true'
        echo 'Pipeline finished'
    }

    success {
        echo 'Build and deployment successful'
    }

    failure {
        echo 'Pipeline failed'
    }
}
