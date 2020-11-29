import subprocess
import argparse
import sys
import os
#from subprocess import check_output


def unzip_forge(args):
    initialDir = os.getcwd()
    res = str(input('Creating folder at {directory} with forge version {forge} called {modid}. [y/N]: '.format(directory=args.directory, forge=args.forge, modid=args.id) ) or 'n').lower()
    if res == 'y':
        print('Yes : ' + res)
        pathToZip = args.forge
        pathToOut = args.directory + '/{modid}'.format(modid=args.id)
        unzip = ['unzip', '-o', pathToZip, '-d', pathToOut]
        p = subprocess.run(unzip, capture_output=True )
        run_gradlew_commands(pathToOut)
        rename_launch_configs(pathToOut, args.id)
        format_package_and_toml(initialDir, pathToOut, args.id)
    elif res == 'n':
        print('User entered N, canceled.')

def run_gradlew_commands(dir):
    os.chdir(dir)
    proc = subprocess.Popen(['./gradlew', 'genEclipseRuns'], stdout=subprocess.PIPE)
    for line in proc.stdout:
        sys.stdout.write(str(line.decode('utf-8')))

def rename_launch_configs(dir, id):
    ext = '.launch'
    for file in os.listdir(dir):
        if file.endswith(ext):
            parts = file.split('.')
            parts[0] = parts[0] + id.capitalize()
            parts[1] = '.' + parts[1]
            filename = ''.join(parts)
            rename = ['mv', file, filename]
            subprocess.run(rename)

def format_package_and_toml(initialDir, dir, id):
    examplemodDir = dir +'/src/main/java/com/example'
    newModDir = dir + '/src/main/java/com/loucaskreger/{id}'.format(id=id.lower())
    resourceDir = dir + '/src/main/resources/META-INF/mods.toml'
    makeDir = ['mkdir', '-p', newModDir]
    moveJava = ['cp', '{initial}/Example.java'.format(initial=initialDir), newModDir + '/{capID}.java'.format(capID=id.capitalize())]
    moveToml = ['cp', '{initial}/mods.toml'.format(initial=initialDir), resourceDir]
    remove = ['rm', '-rf', examplemodDir]
    subprocess.run(makeDir)
    subprocess.run(moveJava)
    subprocess.run(moveToml)
    subprocess.run(remove)
    replace_placeholders([newModDir + '/{capID}.java'.format(capID=id.capitalize()), resourceDir], id)

def replace_placeholders(dirs, id):
    for file in dirs:
        f = open(file, 'r')
        filedata = f.read()
        f.close()
        newdata = filedata.replace('id_placeholder', id.lower())
        newdata = newdata.replace("placeholder", id.capitalize())
        f = open(file, 'w')
        f.write(newdata)
        f.close()


if __name__ == '__main__':
    defaultModdingDir = '/home/loucas/Minecraft Modding'
    parser = argparse.ArgumentParser(description='Sets up forge modding enviroment')
    parser.add_argument('-dir', '--directory', dest='directory', default=defaultModdingDir, type=str, help='The destination directory of the completed setup')
    parser.add_argument('-forge', '-f',required=True, dest='forge', type=str, help='The zipped forge dir to use')
    parser.add_argument('-modid', '-name', '-n', '-id',required=True, dest='id', default='forge', type=str, help='The modid of the mod' )
    args = parser.parse_args()
    unzip_forge(args)
    print(args)
