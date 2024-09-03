echo "I'm another bash script!"


# Let's say this is the main one

cat << EOF | python3 -
import sys
print(f'Python Version: {sys.version}')


import subprocess
if __name__ == '__main__':
    print('Hello World')
    subprocess.run('ls', shell=True)
EOF