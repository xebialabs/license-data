#!groovy

def releaseArgs(params) {
  return (params.RELEASE_EXPLICIT.trim() == '') ?
      "-Prelease.scope=${params.RELEASE_SCOPE} -Prelease.stage=final" :
      "-Prelease.explicit=${params.RELEASE_EXPLICIT}"
}

def supportedBranches = '9.0.x-maintenance 9.5.x-maintenance 9.7.x-maintenance 9.8.x-maintenance master'

String newVersion

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
    string(name: 'PUSHABLE_BRANCHES', defaultValue: supportedBranches, description: 'a space-separated list of branch names that will be updated')
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
        checkout scm

        sh "./gradlew clean build uploadArchives release --no-build-cache ${releaseArgs(params)}"

        script {
          newVersion = readFile('build/version.dump')
        }
      }
    }

    stage('Run Update dependencies') {
      steps {
        script {
          def updateJobs = params.PUSHABLE_BRANCHES.split('\\s+').collectEntries { branch ->
            ["branch $branch", { build([
                job       : "Update dependencies",
                parameters: [
                    string(name: 'branch', value: branch),
                    string(name: 'project', value: 'groupUpdateAllDependencies'),
                    string(name: 'dependency', value: 'licenseDatabaseVersion'),
                    string(name: 'newValue', value: newVersion.substring(newVersion.lastIndexOf('=') + 1))
                ],
                wait      : false
            ]) }]
          }
          parallel(updateJobs)
        }
      }
    }
  }
}
