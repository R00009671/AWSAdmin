import boto

# This class has been implemented to act as a replacement for the Switch Methods found in other languages such as c#
# This recipe was taken from the following website: http://code.activestate.com/recipes/410692/
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def CreateBucket(s3conn):
    global create, bucketName, bucket
    create = raw_input("Would you like to create a bucket?")
    if create == "y":
        bucketName = raw_input("Please enter Name of bucket")

        bucket = s3conn.lookup(bucketName)
        if bucket:
            print "Bucket (%s) allready exists" % bucketName
            CreateBucket(s3conn)
        else:
            try:
                bucket = s3conn.create_bucket(bucketName)
            except s3conn.provider.storage_create_error, e:
                print "The bucket (%s) cannot be created" % bucketName








