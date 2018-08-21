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
		print("Instance Id: "+ info['Findings'][0]['Resource']['InstanceDetails']['InstanceId'])
		print("Instance name: "+ str(info['Findings'][0]['Resource']['InstanceDetails']['Tags']))#[0]['Value'])
		print("Issue count:  " + str(info['Findings'][0]['Service']['Count']))
		print('================================================================')
