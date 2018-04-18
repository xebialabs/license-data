#!groovy


def releaseArgs(params) {
    return (params.RELEASE_EXPLICIT.trim() == '') ?
        "-Prelease.scope=${params.RELEASE_SCOPE} -Prelease.stage=final" :
        "-Prelease.explicit=${params.RELEASE_EXPLICIT}"
}

pipeline {
  agent none

  environment {
    GRADLE_OPTS = '-XX:MaxPermSize=256m -Xmx1024m  -Djsse.enableSNIExtension=false'
  }

  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    skipDefaultCheckout()
    timeout(time: 10, unit: 'MINUTES')
    timestamps()
    ansiColor('xterm')
  }

  parameters {
    choice(name: 'RELEASE_SCOPE', choices: 'patch\nminor\nmajor', description: 'Which version component should be incremented?')
    string(name: 'RELEASE_EXPLICIT', defaultValue: '', description: 'In case of a new development cycle you may need to set the version number explicitly if it is non-contiguous. E.g. put something like 1.2.3 or 1.2.3-beta.10 here.')
  }

  stages {
    stage('Release License Database') {
      agent {
        label 'release||release-xlr||release-xld'
      }

      tools {
        jdk 'JDK 8u60'
      }

      steps {
        //cleanWs()
        checkout scm

        sh "./gradlew clean build uploadArchives release --no-build-cache ${releaseArgs(params)}"

        script {
          newVersion = readFile 'build/version.dump'
        }
      }

//      post {
  //      always {
          // cleanWs()
    //    }
      //}
    }

    stage('Run Update dependencies') {
      steps {
        build job: "Update dependencies",
            parameters: [
                string(name: 'branch', env.BRANCH_NAME),
                string(name: 'project', 'groupUpdateAllDependencies'),
                string(name: 'dependency', 'licenseDatabaseVersion'),
                string(name: 'newValue', value: newVersion)
            ],
            wait: false
      }
    }
  }
}