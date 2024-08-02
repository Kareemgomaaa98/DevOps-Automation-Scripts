# Jenkins Pipeline for MongoDB Backup and Restore

This repository contains a Jenkins pipeline script designed for performing MongoDB backups and restores using AWS S3 for storage. The script is configured to send notifications to a Slack channel.

## Pipeline Overview

The pipeline includes the following main stages:

1. **Connecting to S3**: Verifies the connection to the specified S3 bucket.
2. **Backup or Restore**: Depending on the selected action, either backs up the MongoDB database to S3 or restores it from S3.

## Environment Variables

The following environment variables are used in the pipeline:

- **ACCESS_KEY_ID**: AWS S3 access key ID.
- **SECRET_ACCESS_KEY**: AWS S3 secret access key.
- **DEFAULT_REGION**: AWS S3 region.
- **S3_BUCKET**: S3 bucket name for storing backup files.
- **S3_ENDPOINT**: Endpoint URL for the S3 bucket.
- **SLACK_CHANNEL**: Slack channel for sending notifications.
- **MONGODB_VPS01**: MongoDB credentials.

## Parameters

The pipeline uses a parameter to determine the action to be performed:

- **ACTION**: Can be either `Backup` or `Restore`.

## Pipeline Stages

### Connecting to S3

This stage verifies the connection to the specified S3 bucket by listing the available buckets. Notifications are sent to Slack indicating the connection status.

### Backup or Restore

Depending on the value of the `ACTION` parameter, this stage will either:

- **Backup**: Perform a MongoDB dump, compress the dump into a tarball, and upload it to the S3 bucket.
- **Restore**: Download the backup tarball from the S3 bucket, extract it, and restore the MongoDB database.

## Slack Notifications

The pipeline sends notifications to the specified Slack channel at various stages:

- When connecting to S3.
- When starting and completing the backup or restore process.
- The final status of the pipeline (success, failure, or aborted).

## Script

Below is the Jenkins pipeline script:

```groovy
def slackPostBuild(status) {
    def color = status == 'SUCCESS' ? '#00FF00' : (status == 'FAILURE' ? '#FF0000' : '#808080')
    slackSend(
        channel: SLACK_CHANNEL,
        color: color,
        message: "${status == 'SUCCESS' ? 'SUCCEEDED 🥳' : (status == 'FAILURE' ? 'FAILED 😢' : 'ABORTED 🤒')} : \n" +
                 "Job name: ${JOB_NAME} \n" +
                 "Triggered by Git Commit: ${GIT_COMMIT} \n" +
                 "Branch: ${GIT_BRANCH} \n" +
                 "Git url: ${GIT_URL} \n" +
                 "Build url: ${BUILD_URL} \n" +
                 "Build id: ${BUILD_ID}"
    )
}

pipeline {
    agent {
        kubernetes {
            yamlFile './agent-pod-template.yaml'
        }
    }

    environment {
        ACCESS_KEY_ID     = credentials('s3-access-key')
        SECRET_ACCESS_KEY = credentials('s3-secret-access-key')
        DEFAULT_REGION    = 'sbg'
        S3_BUCKET         = 'databases-backup/mongodb-vps01'
        S3_ENDPOINT       = 'https://s3.sbg.io.cloud.ovh.net/'
        SLACK_CHANNEL     = 'backups_and_restore'
        MONGODB_VPS01     = credentials('mongodb-vps01')
    }

    parameters {
        choice(name: 'ACTION', choices: ['Backup', 'Restore'])
    }

    stages {
        stage('Connecting to S3') {
            steps {
                script {
                    slackSend(channel: SLACK_CHANNEL, color: '#808080', message: "Connecting to S3...")
                    container('ubuntu') {
                        sh '''
                        aws configure set aws_access_key_id ${ACCESS_KEY_ID}
                        aws configure set aws_secret_access_key ${SECRET_ACCESS_KEY}
                        aws configure set region ${DEFAULT_REGION}
                        aws s3 ls --endpoint-url "${S3_ENDPOINT}"
                        '''
                    }
                    slackSend(channel: SLACK_CHANNEL, color: '#00FF00', message: "Connected to S3.")
                }
            }
        }

        stage('Backup or Restore') {
            steps {
                script {
                    if (params.ACTION == 'Backup') {
                        slackSend(channel: SLACK_CHANNEL, color: '#808080', message: "Starting backup process...")
                        container('ubuntu') {
                            sh '''
                            mongodump --out=./backup_files --uri="${MONGODB_VPS01}" && tar -cvzf mongodb-backup-$(date +%F).tar.gz backup_files
                            ls -lh
                            TAR_FILE=$(ls mongodb-backup-*.tar.gz)
                            aws s3 cp $TAR_FILE s3://${S3_BUCKET}/ --endpoint-url "${S3_ENDPOINT}"
                            aws s3 ls s3://${S3_BUCKET}/ --endpoint-url "${S3_ENDPOINT}"
                            rm -r ./backup_files
                            rm mongodb-backup-$(date +%F).tar.gz
                            ls -a
                            '''
                        }
                        slackSend(channel: SLACK_CHANNEL, color: '#00FF00', message: "Backup process completed.")
                    } else if (params.ACTION == 'Restore') {
                        slackSend(channel: SLACK_CHANNEL, color: '#808080', message: "Starting restore process...")
                        container('ubuntu') {
                            sh '''
                            YESTERDAY=$(date -d "yesterday" +%F)
                            aws s3 cp s3://${S3_BUCKET}/mongodb-backup-$YESTERDAY.tar.gz . --endpoint-url "${S3_ENDPOINT}"
                            tar -zxvf mongodb-backup-$YESTERDAY.tar.gz
                            mongorestore --uri="${MONGODB_VPS01}" ./backup_files
                            rm -r ./backup_files
                            rm mongodb-backup-$YESTERDAY.tar.gz
                            ls -a
                            '''
                        }
                        slackSend(channel: SLACK_CHANNEL, color: '#00FF00', message: "Restore process completed.")
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                slackPostBuild(currentBuild.currentResult)
            }
        }
    }
}
