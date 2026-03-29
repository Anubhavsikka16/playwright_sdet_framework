pipeline {
    agent any

    tools {
        python 'python3.11'   // Configure in Jenkins Global Tool Config
        nodejs 'node18'       // Needed for Allure CLI
    }

    environment {
        ENV = 'prod'
    }

    stages {

        stage('Checkout Code') {
            steps {
                 git branch: 'main', url: 'https://github.com/Anubhavsikka16/playwright_sdet_framework.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                 sh '''
                python3 -m venv $ENV
                . $VENV/bin/activate
                pip install --upgrade pip
                pip3 install pytest-playwright
                pip install allure-pytest
                pip install pytest-html
                pip install pytest-xdist 
                '''
            }
        }

        stage('Run Tests') {
            steps {
                withCredentials([
                    string(credentialsId: 'BASE_URL', variable: 'BASE_URL'),
                    string(credentialsId: 'API_BASE_URL', variable: 'API_BASE_URL'),
                    string(credentialsId: 'USERNAME', variable: 'USERNAME'),
                    string(credentialsId: 'PASSWORD', variable: 'PASSWORD')
                ]) {
                    sh '''
                    echo "Running tests..."
                    pytest -v -n auto --alluredir=reports/allure-results
                    '''
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh '''
                allure generate reports/allure-results -o reports/allure-report --clean
                '''
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false,
                       jdk: '',
                       results: [[path: 'reports/allure-results']]
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
        }

        success {
            echo '✅ Tests Passed'
        }

        failure {
            echo '❌ Tests Failed'
        }
    }
}