echo "I'm a bash script!"

cat << EOF | python3 -
import subprocess
if __name__ == '__main__':
    print('Hello World')
    subprocess.run('ls', shell=True)
EOF