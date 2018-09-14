#!/usr/bin/env python3.6

import boto3
import csv
from datetime import datetime, timedelta
from operator import itemgetter

accounts = [
    {
        "name": "pdffiller",
        "region": "us-east-1",
        "env": "prod"
#        "access_key_id": "",
#        "secret_access_key": ""
    }
]

with open('instances.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'AZ', 'ID']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for account in accounts:
        session = boto3.Session(profile_name='pdf-dev')

        ec2 = session.resource('ec2', region_name=account['region'])
        cw = session.client('cloudwatch', region_name=account['region'])

        count = 0

        for instance in ec2.instances.filter():
            count += 1
            print('Handle instance ', count, ' id ', instance.id)

            data = {
                "name": "",
                "AZ": instance.placement["AvailabilityZone"],
                "ID": instance.id,
            }
            if instance.tags:
                for tag in instance.tags:
                    key = tag.get("Key").lower()
                    value = tag.get("Value")

                    if key == "name":
                        data["name"] = value
            writer.writerow(data)
