pipeline {
    agent any

    environment {
        DOCKER_HUB = 'hemanathan18'
        APP_NAME_BACKEND = 'enerops-backend'
        APP_NAME_FRONTEND = 'enerops-frontend'
        EC2_IP = "32.197.41.172"
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

                        // Build & Push Frontend (Nginx /api reverse proxy routing)
                        sh "docker build --build-arg NEXT_PUBLIC_API_URL=http://${EC2_IP}/api -t ${DOCKER_HUB}/${APP_NAME_FRONTEND}:latest ./frontend"
                        sh "docker push ${DOCKER_HUB}/${APP_NAME_FRONTEND}:latest"
                    }
                }
            }
        }

        stage('Deploy to AWS EC2 via SSH') {
            steps {
                script {
                    // Jenkins Credentials-il irundhu Secret File (.env) matrum SSH Key-ai read seigiradhu
                    configFileProvider([configFile(fileId: 'enerops-env-file', variable: 'SECRET_ENV')]) {
                        sshagent(['EC2-SSH']) {
                            sh """
                                # 1. Directory create panni, docker-compose, nginx.conf & Jenkins Secret .env-ai EC2-ukku copy seivadhudhu
                                ssh -o StrictHostKeyChecking=no ubuntu@${EC2_IP} 'mkdir -p ~/enerops'
                                scp -o StrictHostKeyChecking=no docker-compose.yml nginx.conf ubuntu@${EC2_IP}:~/enerops/
                                scp -o StrictHostKeyChecking=no \${SECRET_ENV} ubuntu@${EC2_IP}:~/enerops/.env

                                # 2. EC2-il containers-ai pull panni restart seiyuvadhudhu
                                ssh -o StrictHostKeyChecking=no ubuntu@${EC2_IP} '
                                    cd ~/enerops
                                    docker compose pull
                                    docker compose down
                                    docker compose up -d --remove-orphans
                                '
                            """
                        }
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
