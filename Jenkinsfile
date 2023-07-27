pipeline {
    agent any
    stages {
        stage('Preparation') {
            steps {
                // Install necessary packages
                sh '''
                 whoami
                 sudo apt-get update
                 sudo apt-get install -y python3 python3-pip virtualenv git
                '''
            }
        }
        stage('Checkout') {
            steps {
                // Checkout your Git repository
                 sh 'git --version'
                git -version
                git 'https://github.com/elisonego/FyberProj.git'
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
        stage('Unit Test') {
            steps {
                // This will run your unit tests
                sh '''
                . venv/bin/activate
                python -m unittest myapp.py
                '''
            }
        }
    }
}
