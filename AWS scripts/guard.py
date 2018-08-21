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
		print("Issue type: "+ info['Findings'][0]['Type'])
		print("Issue count:  " + str(info['Findings'][0]['Service']['Count']))
		print("Severity:  " + str(info['Findings'][0]['Severity']))
		print("Instance Id: "+ info['Findings'][0]['Resource']['InstanceDetails']['InstanceId'])
		try:
			for tag in info['Findings'][0]['Resource']['InstanceDetails']['Tags']:
				if tag['Key'] == 'Name':
					print("Instance name: "+tag['Value'])
					break
		except Exception:
			print("No name")
			continue
		print('================================================================')
