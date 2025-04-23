// Jenkinsfile
pipeline {
    agent any // Or specify a node with Docker installed: agent { label 'docker-node' }

    environment {
        // Define environment variables needed for the build/deploy
        // Secrets should be managed via Jenkins Credentials
        // Example: Use 'withCredentials' block for sensitive data
        // DOCKERHUB_CREDENTIALS = credentials('your-dockerhub-credentials-id')
        // DB_PASSWORD = credentials('mysql-db-password-id')
        // SECRET_KEY = credentials('django-secret-key-id')
        // For this example, we assume .env is available locally or variables are set in Jenkins env
        REGISTRY = "yourdockerhubusername/bookstore-app" // Replace with your Docker Hub username/repo
        TAG = "latest"
        COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                // Assumes Jenkins is configured to check out from your Git repository
                checkout scm
            }
        }

        stage('Lint & Security Check (Optional)') {
            steps {
                echo 'Running linters (e.g., flake8, bandit)...'
                // Example: Requires linters installed in the build environment or a Docker container
                // sh 'flake8 .'
                // sh 'bandit -r .'
            }
        }

        stage('Build Docker Image') {
            steps {
                 echo "Building Docker image ${env.REGISTRY}:${env.TAG}..."
                 // Ensure .env file exists or environment vars are correctly set for compose build
                 // Note: docker-compose build might be simpler if compose file is complex
                 sh "docker build -t ${env.REGISTRY}:${env.TAG} ."
            }
        }

        stage('Unit Tests (Example)') {
            steps {
                echo 'Running Django unit tests inside a container...'
                // Use docker-compose to run tests against the db service
                 script {
                    try {
                        // Ensure DB is up if tests require it, or use sqlite for tests
                        // Clean up previous test runs if necessary
                        sh "docker-compose -f ${env.COMPOSE_FILE} down --volumes || true"
                        // Start db service for tests
                        sh "docker-compose -f ${env.COMPOSE_FILE} up -d db"
                        // Run tests in a one-off container linked to the db
                        // Override command to run tests. Ensure env vars are passed.
                        // Use --rm to clean up container after test run
                        sh """
                           docker-compose -f ${env.COMPOSE_FILE} run --rm --entrypoint "python manage.py test" web
                        """
                    } finally {
                         // Ensure services are stopped even if tests fail
                         sh "docker-compose -f ${env.COMPOSE_FILE} down --volumes"
                    }
                 }
            }
        }

        stage('Push Docker Image (Optional)') {
             // Only run if building on master/main or a release branch typically
             // when { branch 'main' }
             steps {
                  echo "Pushing Docker image ${env.REGISTRY}:${env.TAG}..."
                  // Login to Docker Hub (using Jenkins Credentials)
                  // withCredentials([usernamePassword(credentialsId: 'your-dockerhub-credentials-id', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                  //     sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                  // }
                  // sh "docker push ${env.REGISTRY}:${env.TAG}"
             }
        }


        stage('Deploy') {
            // This is a basic deployment using docker-compose up
            // Real-world deployment might involve SSH, Ansible, Kubernetes, etc.
            steps {
                echo "Deploying application using Docker Compose..."
                // Ensure .env file with production settings is present on the target server
                // Or manage secrets securely (e.g., Jenkins Credentials Binding)
                // Stop existing containers (if any) and remove volumes to start fresh (or handle migrations carefully)
                sh "docker-compose -f ${env.COMPOSE_FILE} down --volumes || true"
                 // Pull latest images if pushed in previous stage (or rely on local build)
                 // sh "docker-compose -f ${env.COMPOSE_FILE} pull"
                // Start services in detached mode
                sh "docker-compose -f ${env.COMPOSE_FILE} up -d --build" // --build ensures image is rebuilt if needed
                echo "Deployment complete. Application should be running."
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
             // Clean up workspace, logout from docker etc.
             // sh 'docker logout'
             // cleanWs()
             // Stop compose services if needed for cleanup
             // sh "docker-compose -f ${env.COMPOSE_FILE} down --volumes || true"
        }
        success {
            echo 'Pipeline succeeded!'
            // Send notification (Slack, Email)
        }
        failure {
            echo 'Pipeline failed!'
            // Send notification (Slack, Email)
        }
    }
}