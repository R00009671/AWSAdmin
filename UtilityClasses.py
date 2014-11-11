import boto
import boto.ec2.cloudwatch
# enable line below to turn on the debugger
#boto.set_stream_logger('boto')

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
# read in the repsonse for the menu
 response = raw_input('''Please select What feature you would like to view:
  \n 1 for amazon EC 2 instances
  \n 1.1 to create new isntance
  \n 2 for S3 Bucket listings
  \n 3 Enable cloud watch for All instances ''')

#Using a Switch from UtilityClasses to create the menu system
 for case in switch(response):
    if case('1'):
        print("Running AWS EC2 Instances")
        conn = boto.ec2.connect_to_region(selectRegion)

        #Build an array called Instances and append each instance this via the extend method
        instances = getInstances(selectRegion)
        for i in instances:
            print ("Instance ID:",i ,
                    "Instance Type:", i.instance_type,
                    "Instance Region: ", i.placement,
                    "Instance Launch Time: ", i.launch_time)

        backToMenu()

    elif case('1.1'):
        # create connectyion and pass in connection to new isntance
         conn = boto.ec2.connect_to_region(selectRegion)
         createNewIsntance(conn)

    elif case('2'):
        print("You selected S3 buckets")
        print("Current S3 Buckets:")
        #create connection for s3
        s3conn = boto.connect_s3()
        # get list aof all bucks
        buckets = s3conn.get_all_buckets()

        if not buckets:
            print("No buckets exists you need to create a bucket")
            #Prompt to create a new bucket
            CreateBucket(s3conn)

        else:
            # if there are buckets then show the name then propmt to create a new one via custom methods
            for bucket in buckets:
                print bucket
        CreateBucket(s3conn)
        # call the main menut
        backToMenu()

    elif case('3'):
        print("Enable CloudWatch on all instances")
        cloudwatch(selectRegion)
        backToMenu()


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
# shutdown a particular instance whos isntance id is passed in
        conn.stop_instances(instance)


def backToMenu():

    goBack = raw_input("Go back to main Menu?: ")

    if goBack.lower() == "yes" or "y":
     MainMenu()

def cloudwatch(selectRegion):
    conn  = boto.ec2.connect_to_region(selectRegion)
    print "Enabling ClouwWatch Monitoring On all instances"

    listOfInstances = getInstances(selectRegion)
# enable monitoring for all instance in the list
    for instance in listOfInstances:
        print "Enabled Monitoring of (%s)" % instance.id
        conn.monitor_instance(instance.id)


    create_alarm(selectRegion)

    backToMenu()



def getInstances(selectRegion):

    conn = boto.ec2.connect_to_region(selectRegion)

    #Build an array called Instances and append each instance this via the extend method
    instances = []
    reservations = conn.get_all_reservations()
    for reservation in reservations:
        instances.extend(reservation.instances)

    return  instances

def createNewIsntance(conn):


    ami = "ami-f0b11187"

    reservation = conn.run_instances(ami, instance_type='t2.micro', placement='eu-west-1c')
    print reservation






def create_alarm(selectRegion):



    cw = boto.connect_cloudwatch()
    instance_id = raw_input("Please enter Instance ID")
    alarm_name = raw_input("Please Enter the Alarm name")
    email_addresses = raw_input("Please enter your email address for notification")
    metric_name = "CPUUtilization"
    comparison = ">"
    threshold = "40"
    period = "60"
    eval_periods = "2"
    statistics = "average"

    instance = getInstances(selectRegion)


    sns = boto.connect_sns()

    instance = instance[0]
    instance.monitor()

    # Create the SNS Topic
    topic_name = 'CWAlarm-%s' % alarm_name
    print 'Creating SNS topic: %s' % topic_name
    response = sns.create_topic(topic_name)
    topic_arn = response['CreateTopicResponse']['CreateTopicResult']['TopicArn']
    print 'Topic ARN: %s' % topic_arn

    # Subscribe the email addresses to SNS Topic

    print 'Subscribing %s to Topic %s' % (email_addresses, topic_arn)
    sns.subscribe(topic_arn, 'email', email_addresses)



    metric = cw.list_metrics(dimensions={'InstanceId':instance_id},
                             metric_name=metric_name)[0]


    print 'Creating alarm'
    alarm = metric.create_alarm(name=alarm_name, comparison=comparison,
                                threshold=threshold, period=period,
                                evaluationn_periods=eval_periods,
                                statistics=statistics,
                                alarm_actions=[topic_arn],
                                ok_actions=[topic_arn])
