import string, sys

def main(arg1):
    print (arg1)
    maryvilledev_start = string.find(arg1,"maryvilledev") + 13
    feature_branch_end = string.find(arg1, " ", maryvilledev_start)
    print arg1[maryvilledev_start: feature_branch_end]

if __name__=='__main__':
    main(sys.argv[1])
