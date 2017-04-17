import string, sys, json

def main(arg1):
    print arg1
    message = eval(arg1)['message']
    print message
    maryvilledev_start = string.find(message,'maryvilledev/')
    if maryvilledev_start == -1:
        print("Missing marvyilledev/")
        return -1
    maryvilledev_start+=13
    feature_branch_end = string.find(message, ' ', maryvilledev_start)
    if feature_branch_end == -1:
        print("Missing feature branch end")
        return -1
    print(maryvilledev_start,feature_branch_end)
    print arg1[maryvilledev_start: feature_branch_end]

if __name__=='__main__':
    main(sys.argv[1])
