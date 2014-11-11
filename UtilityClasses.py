import boto
import boto.ec2.cloudwatch

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
#Build Up menu as A function so it can be called in multiple locations
def MainMenu():

 selectRegion =  "eu-west-1"



 response = raw_input('''Please select What feature you would like to view:
  \n 1 for amazon EC 2 instances
  \n 2 for S3 Bucket listings
  \n 3 Enable cloud watch for All instances ''')

#Using a Switch from UtilityClasses to create the menu system
 for case in switch(response):
    if case('1'):
        print("Running AWS EC2 Instances")
        conn = boto.ec2.connect_to_region(selectRegion)

        #Build an array called Instances and append each instance this via the extend method
        instances = []
        reservations = conn.get_all_reservations()
        for reservation in reservations:
            instances.extend(reservation.instances)
         #Print out the information for each instance
        for i in instances:
            print ("Instance ID:",i ,
                    "Instance Type:", i.instance_type,
                    "Instance Region: ", i.placement,
                    "Instance Launch Time: ", i.launch_time)
        launchInstance(conn)
        backToMenu()


    elif case('2'):
        print("You selected S3 buckets")
        print("Current S3 Buckets:")
        s3conn = boto.connect_s3()
        buckets = s3conn.get_all_buckets()

        if not buckets:
            print("No buckets exists you need to create a bucket")
            CreateBucket(s3conn)

        else:
            for bucket in buckets:
                print bucket
        CreateBucket(s3conn)
        backToMenu()

    elif case('3'):
        print("Enable CloudWatch on all instances")
        cloudwatch(selectRegion)



def CreateBucket(s3conn):
    global create, bucketName, bucket
    create = raw_input("Would you like to create a bucket?")
    if create == "y":
        bucketName = raw_input("Please enter Name of bucket")

        if bucket is None:
            return

        bucket = s3conn.lookup(bucketName)
        if bucket:
            print "Bucket (%s) allready exists" % bucketName
            CreateBucket(s3conn)
        else:
            try:
                bucket = s3conn.create_bucket(bucketName)
            except s3conn.provider.storage_create_error, e:
                print "The bucket (%s) cannot be created" % bucketName




def ShutdownInstance(conn):
    global instance
    instance = raw_input("Enter the instance ID that you wish to shutdown")

    if instance is not None:

        conn.stop_instances(instance)

def launchInstance(conn):

    launchins = raw_input("Do you wish to launch an instance")
    if launchins.lower() == "y" or "yes":
        instanceID = raw_input("Please enter Instance ID to Launch")
        conn.run_instances("i-dbeffb99")
    else:
        exit()

def backToMenu():

    goBack = raw_input("Go back to main Menu?: ")

    if goBack.lower() == "yes" or "y":
     MainMenu()

def cloudwatch(selectRegion):
    conn  = boto.ec2.connect_to_region(selectRegion)
    print "Enabling ClouwWatch Monitoring On all instances"

    listOfInstances = getInstances(selectRegion)

    for instance in listOfInstances:

        conn.monitor_instance(instance.id)





def getInstances(selectRegion):

    conn = boto.ec2.connect_to_region(selectRegion)

    #Build an array called Instances and append each instance this via the extend method
    instances = []
    reservations = conn.get_all_reservations()
    for reservation in reservations:
        instances.extend(reservation.instances)

    return  instances

