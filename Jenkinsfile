pipeline {
agent any

environment {
    IMAGE_NAME = 'thiruvenkadam/python-app'
    IMAGE_TAG = "${BUILD_NUMBER}"
    CONTAINER_NAME = 'flask-app'
}

stages {

    stage('Checkout') {
        steps {
            checkout scm
        }
    }

    stage('Verify environment') {
        steps {
            sh '''
            git --version
            docker --version
            python3 --version
            '''
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
            echo "Deploying application with Docker Compose..."

            docker compose down || true
            docker compose up -d --build

            docker ps
            '''
        }
    }

    stage('Health check') {
        steps {
            sh '''
            echo "Checking application health..."

            for i in {1..15}; do
                if curl -fs http://localhost:5000 > /dev/null; then
                    echo "Application is healthy"
                    exit 0
                fi

                echo "Waiting for application... ($i/15)"
                sleep 3
            done

            echo "Health check failed"
            docker logs ${CONTAINER_NAME} || true
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
        sh 'docker ps -a || true'
        sh 'docker logs ${CONTAINER_NAME} || true'
        echo 'Pipeline failed'
    }
}

}
