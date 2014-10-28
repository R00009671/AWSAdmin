
import boto.ec2
import UtilityClasses
print "Hello Welcome to AWSManager"


response = raw_input("How would you like to enter your amazon credentials? select 1 for enter manually select 2 for read from file: ")


for case in UtilityClasses.switch(response):
    if case('1'):
        selectRegion =  raw_input("Please select your region: ")
        accessKey = raw_input("Please enter your access key: ")
        secretKey = raw_input("Please provide your secret key: ")


        break
    if case('2'):
        print "Red from file"


        awsKeyFile = raw_input("Please enter the location of your AWS key file which you downloaded: ")
        f = open(awsKeyFile, 'r')

        accessKey = f.readline()[15:]
        secretKey = f.readline()[13:]
        selectRegion = raw_input("Please enter the region you wish to conenct to: ")

        conn = boto.ec2.connect_to_region(selectRegion,
        aws_access_key_id=accessKey,
        aws_secret_access_key=secretKey)






        break
    if case(): # default, could also just omit condition or 'if True'
        print "Boom!"










reservations = conn.get_all_reservations()
for reservation in reservations:
    print reservation.instances






#TODO change this to read form an aws keyfile specefied by the user and pull in the infroamtion from there



