#!/usr/bin/python3.6
import boto3
import csv

with open("guardduty.csv", 'w', newline='') as csvfile:
	header = ['Description','InstanceId', 'InstanceName', 'Count', 'Severity']
	writer = csv.DictWriter(csvfile, fieldnames = header)
	writer. writeheader()

	session = boto3.Session(profile_name='pdf-prod')
	guardClient = session.client('guardduty')
	detector = guardClient.list_detectors()['DetectorIds'][0]

	findingPaginator = guardClient.get_paginator('list_findings')
	findingsPages = findingPaginator.paginate(
		DetectorId=detector,
		FindingCriteria={
			'Criterion':{
				'severity':{
					'Gte': 7,
					'Lt': 9
				}
			}
		}
	)
	counter = 1;
	for page in findingsPages:
		#print(page)
		for currentFindingId in page['FindingIds']:
			print("Processing finding #"+str(counter))
			#print("ID:"+currentFinding)
			info = guardClient.get_findings(
				DetectorId=detector,
				FindingIds=[currentFindingId]
			)
			findingType =  info['Findings'][0]['Type']
			findingDesc =  info['Findings'][0]['Description']
			#print(findingType)
			findingCount = str(info['Findings'][0]['Service']['Count'])
			#print(findingCount)
			severity = str(info['Findings'][0]['Severity'])
			#print(severity)
			instanceId = info['Findings'][0]['Resource']['InstanceDetails']['InstanceId']
			#print(instanceId)
			try:
				for tag in info['Findings'][0]['Resource']['InstanceDetails']['Tags']:
					if tag['Key'] == 'Name':
						instanceName = tag['Value']
						#print(instanceName)
						break
			except Exception:
				instanceName = "No name"
				#print(instanceName)
				continue
			#print('================================================================')
			row = {
				#'Type': findingType,
				'Description': findingDesc,
				'InstanceId': instanceId,
				'InstanceName': instanceName,
				'Count': findingCount,
				'Severity': severity
			}
			writer.writerow(row)
			counter+=1
