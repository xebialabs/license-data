#!groovy

def releaseArgs(params) {
  return (params.RELEASE_EXPLICIT.trim() == '') ?
      "-Prelease.scope=${params.RELEASE_SCOPE} -Prelease.stage=final" :
      "-Prelease.explicit=${params.RELEASE_EXPLICIT}"
}

def supportedBranches = '24.3.x-maintenance 25.1.x-maintenance 25.3.x-maintenance master'

// Matches DEFAULT_LINUX_JDK_NAME in the xl-release repository's Jenkinsfile - this database is
// consumed by that build, so both run on the same JDK.
def DEFAULT_JDK_NAME = 'OpenJDK 21.0.6'

String newVersion

pipeline {
  agent none

  environment {
    // No -XX:MaxPermSize here: it was removed after Java 8 and is a fatal 'Unrecognized VM
    // option' on JDK 21. -XX:MaxMetaspaceSize is its replacement, as in the xl-release build.
    GRADLE_OPTS = '-Xmx1024m -XX:MaxMetaspaceSize=256m -Djsse.enableSNIExtension=false'
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
    string(name: 'JDK_NAME', defaultValue: DEFAULT_JDK_NAME, description: 'JDK to use for the release build')
  }

  stages {
    stage('Release License Database') {
      agent {
        label 'release||release-xlr||release-xld'
      }

      tools {
        jdk params.JDK_NAME
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
