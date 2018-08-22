#!/usr/bin/python3.6
import boto3
import csv

session = boto3.Session(profile_name='pdf-prod')
guardClient = session.client('guardduty')
detector = guardClient.list_detectors()['DetectorIds'][0]

findingPaginator = guardClient.get_paginator('list_findings')
findingsPages = findingPaginator.paginate(
	DetectorId=detector,
	FindingCriteria={
		'Criterion':{
			'severity':{
				'Gte': 0,
				'Lt': 4
			}
		}
	}
)
for page in findingsPages:
	#print(page)
	for currentFindingId in page['FindingIds']:
		#print("ID:"+currentFinding)
		info = guardClient.get_findings(
			DetectorId=detector,
			FindingIds=[currentFindingId]
		)
		findingType =  info['Findings'][0]['Type']
		print(findingType)
		findingCount = str(info['Findings'][0]['Service']['Count'])
		print(findingCount)
		severity = str(info['Findings'][0]['Severity'])
		print(severity)
		instanceId = info['Findings'][0]['Resource']['InstanceDetails']['InstanceId']
		print(instanceId)
		try:
			for tag in info['Findings'][0]['Resource']['InstanceDetails']['Tags']:
				if tag['Key'] == 'Name':
					instanceName = tag['Value']
					print(instanceName)
					break
		except Exception:
			instanceName = "No name"
			print(instanceName)
			continue
		print('================================================================')
