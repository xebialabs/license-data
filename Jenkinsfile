#!groovy

def releaseArgs(params) {
  return (params.RELEASE_EXPLICIT.trim() == '') ?
      "-Prelease.scope=${params.RELEASE_SCOPE} -Prelease.stage=final" :
      "-Prelease.explicit=${params.RELEASE_EXPLICIT}"
}

def supportedBranches = '7.0.x-maintenance 7.5.x-maintenance 8.0.x-maintenance master'

environment {
  GRADLE_OPTS = '-XX:MaxPermSize=256m -Xmx1024m  -Djsse.enableSNIExtension=false'
}

buildDiscarder(logRotator(numToKeepStr: '10'))
skipDefaultCheckout()
timeout(time: 10, unit: 'MINUTES')
timestamps()
ansiColor('xterm')

parameters {
  choice(name: 'RELEASE_SCOPE', choices: 'patch\nminor\nmajor', description: 'Which version component should be incremented?')
  string(name: 'RELEASE_EXPLICIT', defaultValue: '', description: 'In case of a new development cycle you may need to set the version number explicitly if it is non-contiguous. E.g. put something like 1.2.3 or 1.2.3-beta.10 here.')
  string(name: 'PUSHABLE_BRANCHES', defaultValue: supportedBranches, description: 'a space-separated list of branch names that will be updated')
}

node {
  stage('Release License Database') {
    node('release||release-xlr||release-xld') {

      tools {
        jdk 'JDK 8u60'
      }

      steps {
        checkout scm

        sh "./gradlew clean build uploadArchives release --no-build-cache ${releaseArgs(params)}"

        newVersion = readFile 'build/version.dump'
      }
    }

    stage('Run Update dependencies') {
      parallel {
        params.PUSHABLE_BRANCHES.split('\\w').collect { branch ->
          build job: "Update dependencies on branch $branch",
              parameters: [
                  string(name: 'branch', branch),
                  string(name: 'project', 'groupUpdateAllDependencies'),
                  string(name: 'dependency', 'licenseDatabaseVersion'),
                  string(name: 'newValue', newVersion)
              ],
              wait: false
        }
      }
    }
  }
}