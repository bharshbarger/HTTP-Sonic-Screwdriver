#! /usr/bin/env python

#HSS.py a tool to generically throw usernames at a login or other form to look for timing attacks

#By @arbitrary_code

import argparse
import urllib
import requests
import time
import ssl
import sys


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--url', nargs = 1, help = 'The URL you want to test.')
	parser.add_argument('-p', '--password', nargs = 1, help = 'The password you want to test, default is null')
	parser.add_argument('-d', '--delay', nargs =1, help = 'Delay in seconds to rate limit requests. Default is 2 seconds')
	parser.add_argument('-P', '--postdata', nargs = 1, help='The POST data string to send, contained in single quotes.\nReplace parameter values with a xux for username and xpx for password. \nExample: "User=xux&Password=xpx&Lang=en"')
	parser.add_argument('-e', '--encode', help='Optionally URL encode all POST data', action = 'store_true')
	parser.add_argument('-v', '--verbose', help='enable verbosity', action = 'store_true')
	parser.add_argument('-V', '--verb', nargs=1,help='which http verb to use GET, POST, PUT, DELETE')
	args = parser.parse_args()

	if args.verbose is True:

		print 
		'''
		 _   _ _____ _____ ____    ____              _ 
		| | | |_   _|_   _|  _ \  / ___|  ___  _ __ (_) ___ 	  
		| |_| | | |   | | | |_) | \___ \ / _ \| '_ \| |/ __|     
		|  _  | | |   | | |  __/   ___) | (_) | | | | | (__        
		|_| |_| |_|   |_| |_|     |____/ \___/|_| |_|_|\___|        
		                                                           
		 ____                            _      _                  
		/ ___|  ___ _ __ _____      ____| |_ __(_)_   _____ _ __  
		\___ \ / __| '__/ _ \ \ /\ / / _` | '__| \ \ / / _ \ '__|   
		 ___) | (__| | |  __/\ V  V / (_| | |  | |\ V /  __/ |      
		|____/ \___|_|  \___| \_/\_/ \__,_|_|  |_| \_/ \___|_|     
															       
		HSS - A Generic HTTP Timing Attack tool					   
																   
		v0.1 													   

		'''
		#print args

	print 'HSS started at: '+(time.strftime("%d/%m/%Y - %H:%M:%S"))

	if args.url is None: 
		parser.print_help()
		sys.exit()

	if args.verb is not None:
		if args.verb is 'PUT':print args.verb

	else:
		print '[-] Verb not specified, using POST'
	

	if args.postdata is None:
		postdata = ''
		print '\n[-] No POST data entered! Exiting! Use -h for help\n'
		sys.exit()
	else:
		postdata = ''.join(args.postdata)

	if args.password is not None:
		userPass = ''.join(args.password)

	if args.delay is None:
		delay = float('2')
	else:
		delay = float(str(''.join(args.delay)))

	for u in args.url:
		url = args.url
		if args.verbose is True:print '[i] Url entered is: '.join(url)+'\n'

	if args.password is None:
		userPass = ''

	if args.password is not None:
		userPass = ''.join(args.password)
		postdata = postdata.replace('xpx', str(userPass))

	def request(args, userPass, postdata, delay):
		
		userList=[]

		#open users.txt to read as object f
		with open('users.txt','r') as f: 
			#read the contents into the userList dictionary
			userList =f.read().splitlines()
			#for each line find its index and value
			for i, userID in enumerate(userList):

				if postdata.find('xux'):
					#replace the string with the user id at the first i value
					postdata=postdata.replace('xux', str(userList[i]))

				if postdata.find('xpx'):
					postdata=postdata.replace('xpx', str(userPass))
				
				if postdata.find(str(userList[i-1])):
					postdata=postdata.replace(str(userList[i-1]),str(userList[i]))

				if args.encode is True:
					postdata = urllib.urlencode(str(postdata))

				#add SSL context to handle certs
				context = ssl._create_unverified_context()


				
				for u in url:
					try:
						print url
						#response = urllib.urlopen(''.join(url), postdata, context=context)
						startTime=time.time()
						response = requests.post(u,str(postdata))
						elapsedTime = str(round((time.time()-startTime)*1000.0))
						#if args.verbose is True:print str(response.read())
						if args.verbose is True:print str(response.text)
						print str(elapsedTime)+'ms'+' - '+str(userID)+':'+str(userPass)+' '
					except requests.exceptions.RequestException as e:  # This is the correct syntax
					    print e
					    sys.exit(1)


				#print timing result with userid and pass
				
				#if verbose print the post data too
				if args.verbose is True: print '[i] POST data: '+str(postdata)
				#throttle
				time.sleep(delay)
			


	request(args, userPass, postdata, delay)

if __name__ == '__main__':
    main()
