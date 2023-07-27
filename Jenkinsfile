pipeline {
    agent any
    stages {
        stage('Preparation') {
            steps {
                sh '''
                 whoami
                 sudo apt-get update
                 sudo apt-get install -y python3 python3-pip virtualenv git curl awscli
                 pip install boto3  # AWS SDK for Python
                '''
            }
        }
        stage('Checkout') {
            steps {
                sh 'git --version'
                git branch: 'main', url: 'https://github.com/elisonego/FyberProj.git'
            }
        }
        stage('Setup Python') {
            steps {
                sh '''
                virtualenv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        stage('Check Webpage') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'myawsCred']]) {
                    sh '''
                    status_code=$(curl --write-out '%{http_code}' --silent --output /dev/null http://54.234.189.172:5000/)
                    echo "The HTTP status code is: $status_code" | tee webpage_status.log
                    if [ $status_code -ne 200 ]; then
                        echo "Webpage is not available (status code: $status_code). Failing the build." | tee -a webpage_status.log
                        exit 1
                    fi
                    # Python script to write to DynamoDB
                    python -c "
                    import boto3
                    dynamodb = boto3.resource('dynamodb')
                    table = dynamodb.Table('WebpageStatus')
                    response = table.put_item(
                       Item={
                            'id': '1',
                            'status_code': $status_code
                        }
                    )
                    "
                    '''
                }
            }
        }
        stage('Upload to S3') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'myawsCred']]) {
                    sh '''
                    aws s3 cp webpage_status.log s3://elisonegojenkins/webpage_status.log
                    '''
                }
            }
        }
    }
}
