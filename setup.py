#
# Copyright 2020 Safak Oner.
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------



#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  os
import  subprocess
import  sys
import  shutil
import  platform
from    getpass             import getuser
from    importlib           import import_module
from    distutils.dir_util  import copy_tree


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
def main():

    dry             = False
    clonePackages   = True
    createPaths     = True
    installPySide   = True
    createPackages  = True
    editUserProfile = True
    cleanFolders    = True
    cleanFiles      = True

    #

    setupPath       = os.path.dirname(os.path.abspath(__file__))
    mecoRootPath    = os.path.join(setupPath, 'meco')
    reposPath       = os.path.join(mecoRootPath, 'repos')
    packagePath     = reposPath

    #

    pythonMajorVersion  = sys.version_info[0]
    platformName        = platform.system()

    #

    displayHeader('MECO SETUP')
    displayInfo('Meco will be installed into: {}'.format(mecoRootPath))
    displayInfo('Type YES if you want to continue...')
    if not dry:
        answer = None
        if pythonMajorVersion == 3:
            answer = input()
        else:
            answer = raw_input()

        if not answer in ['yes', 'YES']:
            displayInfo('Setup is aborted by user.')
            return

    #

    if os.path.isdir(mecoRootPath):
        displayInfo('Meco already exists: {}'.format(mecoRootPath), startNewLine=True)
        return

    #

    masterProjectInternalPackages               = ['mApplication',
                                                   'mCore',
                                                   'mDeveloper',
                                                   'mFileSystem',
                                                   'mMayaCore',
                                                   'mMeco',
                                                   'mMecoPackage',
                                                   'mMecoRelease',
                                                   'mMecoSettings',
                                                   'mNukeCore',
                                                   'mNukeExample',
                                                   'mProcess',
                                                   'mQt'
                                                   ]

    masterProjectExternalPackages               = []

    pySidePackageName = ''
    if pythonMajorVersion == 3:
        pySidePackageName = 'extPySide2{}'.format(platformName)
        masterProjectExternalPackages.append(pySidePackageName)
    else:
        if platformName == 'Windows':
            pySidePackageName = 'extPySideP2Windows'
            masterProjectExternalPackages.append(pySidePackageName)
        else:
            pySidePackageName = 'extPySide2P2{}'.format(platformName)
            masterProjectExternalPackages.append(pySidePackageName)

    #

    masterProjectCurrentUserDevelopmentPackages = ['mCore',
                                                   'mDeveloper',
                                                   'mMeco',
                                                   'mMecoSettings'
                                                   ]

    masterProjectOtherUserDevelopmentPackages   = ['mCore',
                                                   'mMayaCore',
                                                   'mNukeCore',
                                                   'mProcess'
                                                   ]

    masterProjectOtherUserStagePackages         = ['mCore']

    #

    vanProjectInternalPackages                  = ['mCore',
                                                   'mMayaCore',
                                                   'mNukeCore'
                                                   ]

    vanProjectExternalPackages                  = []

    #

    vanProjectCurrentUserDevelopmentPackages    = []

    vanProjectOtherUserDevelopmentPackages      = []

    vanProjectOtherUserStagePackages            = []

    #

    packagesToClone = []
    packagesToClone.extend(masterProjectInternalPackages)
    packagesToClone.extend(masterProjectExternalPackages)
    packagesToClone.extend(masterProjectCurrentUserDevelopmentPackages)
    packagesToClone.extend(masterProjectOtherUserDevelopmentPackages)
    packagesToClone.extend(masterProjectOtherUserStagePackages)
    packagesToClone.extend(vanProjectInternalPackages)
    packagesToClone.extend(vanProjectExternalPackages)
    packagesToClone.extend(vanProjectCurrentUserDevelopmentPackages)
    packagesToClone.extend(vanProjectOtherUserDevelopmentPackages)
    packagesToClone.extend(vanProjectOtherUserStagePackages)
    packagesToClone = list(set(packagesToClone))

    if clonePackages:

        if not os.path.isdir(reposPath):
            os.makedirs(reposPath)

        for package in packagesToClone:

            packageClonePath = os.path.join(reposPath, package)
            if os.path.isdir(packageClonePath):
                continue

            repo = 'https://github.com/safakoner/{}.git'.format(package)

            displayInfo('Cloning package: {}'.format(package))

            popen = subprocess.Popen('git clone {} {}'.format(repo, packageClonePath),
                                     cwd=None,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=True)

            stdOut, stdErr = popen.communicate()
            if stdErr:
                print(stdErr.decode('utf-8'))

    #

    currentUser     = getuser()
    otherUserName   = 'wade'

    # MASTER
    masterProjectInternalPackagesPath               = os.path.join(mecoRootPath,
                                                                   'master',
                                                                   'internal')

    masterProjectExternalPackagesPath               = os.path.join(mecoRootPath,
                                                                   'master',
                                                                   'external')

    masterProjectCurrentUserDevelopmentPackagesPath = os.path.join(mecoRootPath,
                                                                   'master',
                                                                   'developers',
                                                                   currentUser,
                                                                   'development',
                                                                   'main')

    masterProjectOtherUserDevelopmentPackagesPath   = os.path.join(mecoRootPath,
                                                                   'master',
                                                                   'developers',
                                                                   otherUserName,
                                                                   'development',
                                                                   'main')

    masterProjectOtherUserStagePackagesPath         = os.path.join(mecoRootPath,
                                                                   'master',
                                                                   'developers',
                                                                   otherUserName,
                                                                   'stage',
                                                                   'main')

    # VAN
    vanProjectInternalPackagesPath                  = os.path.join(mecoRootPath,
                                                                   'van',
                                                                   'internal')

    vanProjectExternalPackagesPath                  = os.path.join(mecoRootPath,
                                                                   'van',
                                                                   'external')

    vanProjectCurrentUserDevelopmentPackagesPath    = os.path.join(mecoRootPath,
                                                                   'van',
                                                                   'developers',
                                                                   currentUser,
                                                                   'development',
                                                                   'main')

    vanProjectOtherUserDevelopmentPackagesPath      = os.path.join(mecoRootPath,
                                                                   'van',
                                                                   'developers',
                                                                   otherUserName,
                                                                   'development',
                                                                   'main')

    vanProjectOtherUserStagePackagesPath            = os.path.join(mecoRootPath,
                                                                   'van',
                                                                   'developers',
                                                                   otherUserName,
                                                                   'stage',
                                                                   'main')

    #

    if createPaths:

        displayHeader('CREATING PATHS')

        paths = [masterProjectInternalPackagesPath,
                 masterProjectExternalPackagesPath,
                 masterProjectCurrentUserDevelopmentPackagesPath,
                 masterProjectOtherUserDevelopmentPackagesPath,
                 masterProjectOtherUserStagePackagesPath,
                 vanProjectInternalPackagesPath,
                 vanProjectExternalPackagesPath,
                 vanProjectOtherUserDevelopmentPackagesPath,
                 vanProjectOtherUserStagePackagesPath
                 ]

        for path in paths:
            if not os.path.isdir(path):
                os.makedirs(path)

            displayInfo('Path created: {}'.format(path))

    #

    if installPySide:

        displayHeader('INSTALLING PYSIDE')
        setupPySide(reposPath, pySidePackageName, platformName, pythonMajorVersion)

    #

    if createPackages:

        displayHeader('CREATING PACKAGES')

        for package in masterProjectInternalPackages:
            copyVersionedPackage(packagePath, package, masterProjectInternalPackagesPath)

        for package in masterProjectExternalPackages:
            copyVersionedPackage(packagePath, package, masterProjectExternalPackagesPath)


        for package in masterProjectCurrentUserDevelopmentPackages:
            copyNonVersionedPackage(packagePath, package, masterProjectCurrentUserDevelopmentPackagesPath)

        for package in masterProjectOtherUserDevelopmentPackages:
            copyNonVersionedPackage(packagePath, package, masterProjectOtherUserDevelopmentPackagesPath)

        for package in masterProjectOtherUserStagePackages:
            copyNonVersionedPackage(packagePath, package, masterProjectOtherUserStagePackagesPath)

            #

        for package in vanProjectInternalPackages:
            copyVersionedPackage(packagePath, package, vanProjectInternalPackagesPath)

        for package in vanProjectExternalPackages:
            copyVersionedPackage(packagePath, package, vanProjectExternalPackagesPath)


        for package in vanProjectCurrentUserDevelopmentPackages:
            copyNonVersionedPackage(packagePath, package, vanProjectCurrentUserDevelopmentPackagesPath)

        for package in vanProjectOtherUserDevelopmentPackages:
            copyNonVersionedPackage(packagePath, package, vanProjectOtherUserDevelopmentPackagesPath)

        for package in vanProjectOtherUserStagePackages:
            copyNonVersionedPackage(packagePath, package, vanProjectOtherUserStagePackagesPath)

    #

    if editUserProfile:

        displayHeader('EDITING USER PROFILE')

        if platformName == 'Windows':
            editWindowsUserProfile(platformName, packagePath, setupPath)
        else:
            editLinuxMacUserProfile(platformName, packagePath, setupPath)

    #

    if cleanFolders:

        displayHeader('CLEANING (this may take a while)')
        try:
            shutil.rmtree(reposPath)
            displayInfo('Removed: {}'.format(reposPath))
        except Exception as error:
            displayInfo('Please delete the following folder since this script has no permission to do so:',
                        startNewLine=True)
            displayInfo(reposPath, startNewLine=False)
            displayInfo('')

    if cleanFiles:

        thisFile = os.path.abspath(__file__)

        try:
            os.remove(thisFile)
            displayInfo('Removed: {}'.format(thisFile))
        except Exception as error:
            displayInfo('Please delete the following file since this script has no permission to do so:',
                        startNewLine=True)
            displayInfo(reposPath, startNewLine=False)
            displayInfo('')

    #

    displayHeader('MECO SETUP IS COMPLETE')
    displayInfo('Please visit the following link for tutorials and documentation.')
    displayInfo('https://meco.safakoner.com')
    displayInfo('')

def setupPySide(reposPath, pySidePackageName, platformName, pythonMajorVersion):

    pySidePackagePythonPath = os.path.join(reposPath, pySidePackageName, 'python')

    command = ''
    if pythonMajorVersion == 3:
        command = 'pip3 install PySide2 --target="{}"'.format(pySidePackagePythonPath)
    else:
        if platformName == 'Windows':
            command = 'pip install PySide --target="{}"'.format(pySidePackagePythonPath)
        else:
            command = 'pip install PySide2 --target="{}"'.format(pySidePackagePythonPath)

    displayInfo('This may take a while...')

    try:

        popen = subprocess.Popen(command,
                                 cwd=None,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=True)

        stdOut, stdErr = popen.communicate()

        if stdErr and not 'WARNING: You are using pip version' in stdErr.decode('utf-8'):
            print(stdErr)
        else:
            displayInfo('PySide has been installed: {}'.format(pySidePackagePythonPath))

    except Exception as error:

        displayInfo(str(error))

def editLinuxMacUserProfile(platformName, packagePath, setupPath):

    homeDir     = os.path.expanduser('~')
    profileFile = '.bash_profile'

    if platformName == 'Linux':
        profileFile = '.bashrc'

    profileFile = os.path.join(homeDir, profileFile)

    if not os.path.isfile(profileFile):
        open(profileFile, 'w').close()
    else:
        file = open(profileFile, 'r')
        content = file.read()
        file.close()

        if '_mMecoBashProfileMain' in content:
            message = 'Profile file already has Meco function: {}'.format(profileFile)
            displayInfo(message)
            return

    sourceProfileFile = os.path.join(packagePath, 'mMeco', 'script', 'shell', 'mmeco-bash-profile.sh')
    if not os.path.isfile(sourceProfileFile):
        message = 'Source profile file does not exist: {}'.format(sourceProfileFile)
        displayInfo(message)
        return

    file = open(sourceProfileFile, 'r')
    content = file.read()
    file.close()

    content = content.replace('export MECO_PATH="$HOME/_development";', 'export MECO_PATH="{}";'.format(setupPath))

    file = open(profileFile, 'a')
    file.write(content)
    file.close()

    displayInfo('Profile file has been edited: {}'.format(profileFile))

def editWindowsUserProfile(platformName, packagePath, setupPath):

    profileFilePath = os.path.join(os.path.expanduser('~'), 'Documents', 'WindowsPowerShell')
    if not os.path.isdir(profileFilePath):
        os.makedirs(profileFilePath)

    profileFilePath = os.path.join(profileFilePath, 'Microsoft.PowerShell_profile.ps1')

    if not os.path.isfile(profileFilePath):
        open(profileFilePath, 'w').close()
    else:
        file = open(profileFilePath, 'r')
        content = file.read()
        file.close()

        if '_mMecoBashProfileMain' in content:
            message = 'Profile file already has Meco function: {}'.format(profileFilePath)
            displayInfo(message)
            return

    sourceProfileFilePath = os.path.join(packagePath, 'mMeco', 'script', 'powershell', 'mmeco-powershell-profile.ps1')
    if not os.path.isfile(sourceProfileFilePath):
        message = 'Source profile file does not exist: {}'.format(sourceProfileFilePath)
        displayInfo(message)
        return

    file = open(sourceProfileFilePath, 'r')
    content = file.read()
    file.close()

    content = content.replace('$env:MECO_PATH="C:"', '$env:MECO_PATH="{}"'.format(setupPath))

    file = open(profileFilePath, 'a')
    file.write(content)
    file.close()

    displayInfo('Profile file has been edited: {}'.format(profileFilePath))

def copyVersionedPackage(sourcePath, packageName, destinationPath):

    sourcePath = os.path.join(sourcePath, packageName)
    pythonPath = os.path.join(sourcePath, 'python')
    sys.path.insert(0, pythonPath)

    packageInfoModule = import_module('{}.packageInfoLib'.format(packageName))
    destinationPath = os.path.join(destinationPath, packageName, packageInfoModule.VERSION, packageName)

    if not os.path.isdir(sourcePath):
        displayInfo('Package doesn\'t exist: {}'.format(sourcePath))
        sys.path.pop(0)
        return

    if not os.path.isdir(destinationPath):
        copy_tree(sourcePath, destinationPath)

    sys.path.pop(0)

    displayInfo('Package created: {}'.format(destinationPath))

def copyNonVersionedPackage(sourcePath, packageName, destinationPath):

    sourcePath      = os.path.join(sourcePath, packageName)
    destinationPath = os.path.join(destinationPath, packageName)

    if not os.path.isdir(sourcePath):
        displayInfo('Package doesn\'t exist: {}'.format(sourcePath))
        return

    if not os.path.isdir(destinationPath):
        copy_tree(sourcePath, destinationPath)

    displayInfo('Package created: {}'.format(destinationPath))

def displayHeader(header):

    sys.stdout.write('\n{}\n{}\n{}\n'.format('-' * 100, header, '-' * 100))

def displayInfo(message, startNewLine=False, endNewLine=True):

    sys.stdout.write('{}{}{}'.format('\n' if startNewLine else '', message, '\n' if endNewLine else ''))

if __name__ == '__main__':

    main()

