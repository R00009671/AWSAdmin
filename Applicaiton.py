
import boto
import UtilityClasses
print "Hello Welcome to AWSManager"

selectRegion =  "eu-west-1"



response = raw_input('''Please select What feature you would like to view:
  \n 1 for amazon EC 2 instances
  \n 2 for S3 Bucket listings
  \n 3 Enable cloud watch for ''')


for case in UtilityClasses.switch(response):
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
                    "Instance Region: ", i.placement)




        break
    if case('2'):
        print("You selected S3 buckets")

        print("Current S3 Buckets")


        conn = boto.connect_s3()
        buckets = conn.get_all_buckets()

        if not buckets:
            print("No buckets exists")
        else:
            for bucket in buckets:
                print bucket


#Conenct to EC2 and display current instances of EC 2















#TODO change this to read form an aws keyfile specefied by the user and pull in the infroamtion from there



