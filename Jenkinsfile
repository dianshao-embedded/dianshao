pipeline {
    agent any

    environment {
        DIANSHAO_YOCTO_PROJECT_PATH = '/home/geesat/dianshao/dianshao_yocto'
    }

    stages {
        stage('container down') {
            steps {
                sudo sh '/usr/local/bin/docker-compose -f docker-compose-using-host-network.yml down'
            }
        }
        
        stage('image build') {
            steps {
                sudo sh '/usr/local/bin/docker-compose -f docker-compose-using-host-network.yml build'
            }
        }
        
        stage('container deploy') {
            steps {
                sudo sh '/usr/local/bin/docker-compose -f docker-compose-using-host-network.yml up -d'
            }
        }
    }
}