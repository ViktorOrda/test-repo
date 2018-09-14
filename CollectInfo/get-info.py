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

date_to = datetime.utcnow()
date_from = date_to - timedelta(days=30)

with open('instances.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'AZ', 'account', 'component', 'env', 'team', 'server_type', 'creation_date', 'last_month_utilization_rate', 'description']
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

            results = cw.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance.id}],
                StartTime=date_from,
                EndTime=date_to,
                Period=2592000,
                Statistics=['Average'])

            try:
                data_points = results['Datapoints']
                data_point = sorted(data_points, key=itemgetter('Timestamp'))[0]
                utilization = data_point['Average']
                load = round(utilization, 2)
            except IndexError as e:
                load = 0

            data = {
                "name": "",
                "AZ": instance.placement["AvailabilityZone"],
                "account": account['name'],
                "component": "",
                "env": account['env'],
                "team": "",
                "server_type": instance.instance_type,
                "creation_date": instance.launch_time,
                "last_month_utilization_rate": load,
                "description": ""
            }
            if instance.tags:
                for tag in instance.tags:
                    key = tag.get("Key").lower()
                    value = tag.get("Value")

                    if key == "name":
                        data["name"] = value
                        continue

                    if key == "env":
                        data["env"] = value
                        continue

                    if key == "team":
                        data["team"] = value

            writer.writerow(data)
