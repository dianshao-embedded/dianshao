pipeline {
    agent any

    environment {
        DIANSHAO_YOCTO_PROJECT_PATH = '/home/geesat/dianshao/dianshao_yocto'
    }

    stages {
        stage('container down') {
            steps {
                sh 'sudo /usr/local/bin/docker-compose -f docker-compose-using-host-network.yml down'
            }
        }
        
        stage('image build') {
            steps {
                sh 'sudo /usr/local/bin/docker-compose -f docker-compose-using-host-network.yml build'
            }
        }
        
        stage('container deploy') {
            steps {
                sh 'sudo /usr/local/bin/docker-compose -f docker-compose-using-host-network.yml up -d'
            }
        }
    }
}