import boto3


ec2 = boto3.client(
    "ec2",
    region_name="ap-south-1"
)


def list_instances():

    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:

        for instance in reservation["Instances"]:

            instances.append({
                "instance_id": instance["InstanceId"],
                "state": instance["State"]["Name"],
                "instance_type": instance["InstanceType"]
            })

    return instances


def launch_instance(instance_name):

    response = ec2.run_instances(

        ImageId="ami-007b1f3fdea0383d9",

        InstanceType="t3.micro",

        MinCount=1,

        MaxCount=1,

        SubnetId="subnet-0e9ffa766d81e2066",

        SecurityGroupIds=[
            "sg-049dcd9b64b5987a5"
        ],

        TagSpecifications=[
            {
                "ResourceType": "instance",

                "Tags": [
                    {
                        "Key": "Name",
                        "Value": instance_name
                    }
                ]
            }
        ]
    )

    instance_id = response["Instances"][0]["InstanceId"]

    print(
        f"EC2 instance launched successfully: {instance_id}"
    )

    return instance_id


def start_instance(instance_id):

    ec2.start_instances(
        InstanceIds=[instance_id]
    )

    print(
        "EC2 instance start command sent successfully!"
    )


def stop_instance(instance_id):

    ec2.stop_instances(
        InstanceIds=[instance_id]
    )

    print(
        "EC2 instance stop command sent successfully!"
    )


def terminate_instance(instance_id):

    ec2.terminate_instances(
        InstanceIds=[instance_id]
    )

    print(
        "EC2 instance termination command sent successfully!"
    )


if __name__ == "__main__":

    print("Checking EC2 instances...")

    instances = list_instances()

    if instances:

        for instance in instances:

            print(instance)

    else:

        print("No EC2 instances found.")