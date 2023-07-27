pipeline {
    agent any
    stages {
        stage('Preparation') {
            steps {
                // Install necessary packages
                sh '''
                 whoami
                 sudo apt-get update
                 sudo apt-get install -y python3 python3-pip virtualenv git curl
                '''
            }
        }
        stage('Checkout') {
            steps {
                sh 'git --version'
                // Checkout your Git repository
                git branch: 'main', url: 'https://github.com/elisonego/FyberProj.git'
            }
        }
        stage('Setup Python') {
            steps {
                // This will setup Python environment on Jenkins Agent
                sh '''
                virtualenv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        stage('Check Webpage') {
            steps {
                // This will check the status code of the webpage
                sh '''
                status_code=$(curl --write-out '%{http_code}' --silent --output /dev/null http://54.234.189.172:5000/)
                echo "The HTTP status code is: $status_code"
                if [ $status_code -ne 200 ]; then
                    echo "Webpage is not available (status code: $status_code). Failing the build."
                    exit 1
                fi
                '''
            }
        }
    }
}
