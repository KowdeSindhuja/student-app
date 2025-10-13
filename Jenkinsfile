pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "YOUR_DOCKERHUB_USERNAME/student-app"
    IMAGE_TAG = "${env.BUILD_NUMBER}"  // or use git commit: sh 'git rev-parse --short HEAD'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        script {
          // Get short commit hash
          shortCommit = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
          env.IMAGE_TAG = "${shortCommit}"
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          sh "docker build -t ${DOCKERHUB_REPO}:${IMAGE_TAG} ."
          sh "docker tag ${DOCKERHUB_REPO}:${IMAGE_TAG} ${DOCKERHUB_REPO}:latest"
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
          sh "docker push ${DOCKERHUB_REPO}:${IMAGE_TAG}"
          sh "docker push ${DOCKERHUB_REPO}:latest"
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        // Use kubeconfig file stored in Jenkins credentials (as "kubeconfig")
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
          // Update deployment image to new tag and apply
          sh """
            export KUBECONFIG=$KUBECONFIG_FILE
            kubectl set image deployment/student-app-deployment student-app=${DOCKERHUB_REPO}:${IMAGE_TAG} --record || true
            kubectl apply -f k8s/service.yaml
          """
        }
      }
    }
  }

  post {
    success {
      echo "Deployment successful: ${DOCKERHUB_REPO}:${IMAGE_TAG}"
    }
    failure {
      echo "Pipeline failed."
    }
  }
}
