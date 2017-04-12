import os

# import boto3
#
# s3 = boto3.resource('s3')
# bucket = s3.Bucket(os.environ['BUCKET_NAME'])

def get_dirs (bucket):
    """Takes an s3 bucket and creates a dict of dir names to snippet names"""
    dirs = {}
    for obj in bucket.objects.all():
        dirname = os.path.dirname(obj.key)
        basename = os.path.basename(obj.key)
        if not dirname in dirs:
            dirs[dirname] = [basename]
        else:
            dirs[dirname].append(basename)
    return dirs

def has_index (files):
    """Takes the contents of a folder and returns if there is an index file"""
    return 'index.json' in files

def create_index (files):
    """Takes a list of files and creates a dict that is an index of the files"""
    pass
