import string, sys, json

def findFeatureFromMessage(commitBody):
    commitBody = json.loads(commitBody)
    message = commitBody['message']
    print message
    maryvilledev_start = string.find(message,'maryvilledev/')
    if maryvilledev_start == -1:
        print "Start missing"
        return -1
    maryvilledev_start+=13
    feature_branch_end = string.find(message, ' ', maryvilledev_start)
    if feature_branch_end == -1:
        return -1

    feature = message[maryvilledev_start: feature_branch_end]
    print feature
    return feature

def main(arg1):
    return findFeatureFromMessage(arg1)

if __name__=='__main__':
    main(sys.argv[1])
