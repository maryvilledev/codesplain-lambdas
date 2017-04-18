import string, sys, json

def findFeatureFromMessage(commitBody):
    commitBody = json.loads(commitBody)
    message = commitBody['message']
    maryvilledev_start = string.find(message,'maryvilledev/')
    if maryvilledev_start == -1:
        return -1
    maryvilledev_start+=13
    feature_branch_end = string.find(message, '\n', maryvilledev_start)
    if feature_branch_end == -1:
        return -1

    feature = message[maryvilledev_start: feature_branch_end]
    return feature

def main(arg1):
    print findFeatureFromMessage(arg1)

if __name__=='__main__':
    main(sys.argv[1])
