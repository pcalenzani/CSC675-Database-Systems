Set file permission of pem key with following command:
	chmod 400 675team7.pem

Log into the webserver with following command (This command must be executed in the folder with the above .pem key):
	ssh -i "675team7.pem" ubuntu@ec2-18-223-133-52.us-east-2.compute.amazonaws.com

Within the server, log into mysql with the following command (PASSWORD: 'team7'):
	mysql -u root -p
