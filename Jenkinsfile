pipeline {
    agent any
    environment {
        AWS_CREDS = credentials('myawsCred') // The ID you assigned to your AWS credentials
    }
    stages {
        stage('Preparation') {
            steps {
                // Install necessary packages
                sh '''
                 whoami
                 sudo apt-get update
                 sudo apt-get install -y python3 python3-pip virtualenv git curl awscli
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
                echo "The HTTP status code is: $status_code" | tee webpage_status.log
                if [ $status_code -ne 200 ]; then
                    echo "Webpage is not available (status code: $status_code). Failing the build." | tee -a webpage_status.log
                    exit 1
                fi
                '''
            }
        }
        stage('Upload to S3') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'myawsCred', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    sh '''
                    aws s3 cp webpage_status.log s3://elisonegojenkins/webpage_status.log
                    '''
                }
            }
        }
    }
}
