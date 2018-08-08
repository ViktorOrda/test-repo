#!/usr/bin/python3.6
import boto3
import csv

with open("cluster_resources.csv", 'w', newline='') as csvfile:
	header = ['Cluster', 'Free CPU units', 'Free memory']
	writer = csv.DictWriter(csvfile, fieldnames = header)
	writer.writeheader()

	session = boto3.Session(profile_name='pdf-dev')
	ecsClient = session.client('ecs')

	clusterPaginator = ecsClient.get_paginator('list_clusters')
	clusterPages = clusterPaginator.paginate(
		PaginationConfig={
                        'MaxItems': 1000,
                        'PageSize': 50
                }
        )
	
	counter = 1;
	for page in clusterPages:
	#allClusters = ecsClient.list_clusters()
		for currentCluster in page['clusterArns']:
			print ("Processing cluster #"+str(counter))
			clusterCPU = 0
			clusterRAM = 0
			allInstances = ecsClient.list_container_instances(
				cluster = currentCluster	
			)
			for instance in allInstances['containerInstanceArns']:
				info = ecsClient.describe_container_instances(
					cluster = currentCluster,
					containerInstances=[instance]
				)
				resources = info['containerInstances'][0]['remainingResources']
				availableCPU = ""
				availableRAM = ""
				for availableResource in resources:
					if availableResource['name']=='CPU':
						clusterCPU+=availableResource['integerValue']
					if availableResource['name']=='MEMORY':
						clusterRAM+=availableResource['integerValue']
			row = {
				'Cluster': currentCluster.split('/')[1],
				'Free CPU units': str(clusterCPU),
				'Free memory': str(clusterRAM)
			}
			writer.writerow(row)
			counter+=1
