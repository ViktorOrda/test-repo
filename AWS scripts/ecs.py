#!/usr/bin/python3.6
import boto3
import csv

with open("instance_resources.csv", 'w', newline='') as csvfile:
	header = ['Cluster', 'Container instance', 'Free CPU units', 'Free memory']
	writer = csv.DictWriter(csvfile, fieldnames = header)
	writer.writeheader()

	session = boto3.Session(profile_name='pdf-dev')
	ecsClient = session.client('ecs')

	clustersPaginator = ecsClient.get_paginator('list_clusters')
	clusterPages = clustersPaginator.paginate(
		PaginationConfig={
			'MaxItems': 1000,
			'PageSize': 50
		}
	)
	
	counter = 1
	for page in clusterPages:
		#print(page)
		#allClusters = ecsClient.list_clusters()
		for currentCluster in page['clusterArns']:
			print ("Processing cluster #"+str(counter))
			#print ("Cluster: "+currentCluster)
			allInstances = ecsClient.list_container_instances(
				cluster = currentCluster	
			)
			for instance in allInstances['containerInstanceArns']:
				#print ("Instance: "+instance)
				info = ecsClient.describe_container_instances(
					cluster = currentCluster,
					containerInstances=[instance]
				)
				resources = info['containerInstances'][0]['remainingResources']
				availableCPU = ""
				availableRAM = ""
				for availableResource in resources:
					#print(availableResource)
					if availableResource['name']=='CPU':
						availableCPU = str(availableResource['integerValue'])
					#	print("Available CPU units: "+str(availableResource['integerValue']))
					if availableResource['name']=='MEMORY':
						availableRAM = str(availableResource['integerValue'])
					#	print("Available memory units: "+str(availableResource['integerValue']))
				row = {
					'Cluster': currentCluster,
					'Container instance': instance, 
					'Free CPU units': availableCPU,
					'Free memory': availableRAM
				}
				writer.writerow(row)
			counter+=1
	#print (allClusters['clusterArns'])
