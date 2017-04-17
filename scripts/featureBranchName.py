import string, sys, json

def main(arg1):
    message = eval(arg1)['message']
    maryvilledev_start = string.find(message,'maryvilledev/')
    if maryvilledev_start == -1:
        print -1
        return
    maryvilledev_start+=13
    feature_branch_end = string.find(message, ' ', maryvilledev_start)
    if feature_branch_end == -1:
        print -1
        return
    print message[maryvilledev_start: feature_branch_end]

if __name__=='__main__':
    main(sys.argv[1])
