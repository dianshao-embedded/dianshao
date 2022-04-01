pipeline {
    agent any 
    stages {
        stage('container down') {
            steps {
                sh '/usr/local/bin/docker-compose -f docker-compose-using-host-network.yml down'
            }
        }
        
        stage('image build') {
            steps {
                sh '/usr/local/bin/docker-compose -f docker-compose-using-host-network.yml build'
            }
        }
        
        stage('container deploy') {
            steps {
                sh '/usr/local/bin/docker-compose -f docker-compose-using-host-network.yml up -d'
            }
        }
    }
}