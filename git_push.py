import argparse, subprocess

def push_to_repo(commitmessage):
    print(commitmessage)
    a = subprocess.run(['git','add','.'])
    if a.returncode == 0:
        print("added")
    b = subprocess.run(['git','commit','-m',f'{commitmessage}'])
    if b.returncode == 0:
        print("committed")
    r = subprocess.run(['git','push','origin','master'])
    if r.returncode == 0:
        print("pushed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-m", "--message", help="The commit message")

    args = parser.parse_args()
    push_to_repo(vars(args)['message'])