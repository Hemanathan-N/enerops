pipeline {
    agent any

    environment {
        DOCKER_HUB = 'hemanathan18'
        APP_NAME_BACKEND = 'enerops-backend'
        APP_NAME_FRONTEND = 'enerops-frontend'
        EC2_IP = "18.207.109.73"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/Hemanathan-N/enerops.git'
            }
        }

        stage('Build & Push Docker Images') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'DockerHub', usernameVariable: 'docker_un', passwordVariable: 'docker_pwd')]) {
                        sh "docker login -u ${docker_un} -p ${docker_pwd}"
                        
                        // Build & Push Backend
                        sh "docker build -t ${DOCKER_HUB}/${APP_NAME_BACKEND}:latest ./backend"
                        sh "docker push ${DOCKER_HUB}/${APP_NAME_BACKEND}:latest"

                        // Build & Push Frontend
                        sh "docker build -t ${DOCKER_HUB}/${APP_NAME_FRONTEND}:latest ./frontend"
                        sh "docker push ${DOCKER_HUB}/${APP_NAME_FRONTEND}:latest"
                    }
                }
            }
        }

        stage('Deploy to AWS EC2 via SSH') {
            steps {
                script {
                    sshagent(['EC2-SSH']) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ubuntu@${EC2_IP} 'mkdir -p ~/enerops'
                            scp -o StrictHostKeyChecking=no docker-compose.yml ubuntu@${EC2_IP}:~/enerops/
                            ssh -o StrictHostKeyChecking=no ubuntu@${EC2_IP} '
                                cd ~/enerops
                                docker compose pull
                                docker compose down
                                docker compose up -d
                            '
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout'
            cleanWs()
        }
    }
}
