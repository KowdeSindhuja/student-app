pipeline {
  agent any 
  stages {
    stage("Build Docker Image") {
      steps {
        echo "Build Docker Image"
        bat "docker build -t student-app:latest ."
      }
    }
    stage("Docker login") {
      steps {
        bat "docker login -u kowdesindhuja -p 123456789"
      }
    }
    stage("push Docker image to docker hub") {
      steps {
        echo "push Docker image to docker hub"
        bat "docker rmi -f kowdesindhuja/student-app:latest || echo Image not found, skipping"
        bat "docker tag student-app:latest kowdesindhuja/student-app:latest"
        bat "docker push kowdesindhuja/student-app:latest"
      }
    }
    stage("Deploy to kubernetes") {
      steps {
        bat "kubectl apply -f deployment.yaml --validate=false"
        bat "kubectl apply -f service.yaml"
      }
    }
  }
}