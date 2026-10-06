import boto3

s3 = boto3.client(
    "s3",
    region_name="ap-south-1"
)


def list_buckets():

    response = s3.list_buckets()

    buckets = [
        bucket["Name"]
        for bucket in response["Buckets"]
    ]

    return buckets


def create_bucket(bucket_name):

    response = s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            "LocationConstraint": "ap-south-1"
        }
    )

    print("Bucket created successfully!")

    return response


def upload_file(file, bucket_name, object_name):

    s3.upload_fileobj(
        file,
        bucket_name,
        object_name
    )

    print("File uploaded successfully!")


def list_files(bucket_name):

    response = s3.list_objects_v2(
        Bucket=bucket_name
    )

    files = []

    if "Contents" in response:

        for obj in response["Contents"]:

            files.append({
                "name": obj["Key"],
                "size": obj["Size"]
            })

    return files


def download_file(
    bucket_name,
    object_name,
    download_path
):

    s3.download_file(
        bucket_name,
        object_name,
        download_path
    )

    print("File downloaded successfully!")


def delete_file(
    bucket_name,
    object_name
):

    s3.delete_object(
        Bucket=bucket_name,
        Key=object_name
    )

    print("File deleted successfully!")


if __name__ == "__main__":

    print("Checking S3 buckets...")

    buckets = list_buckets()

    for bucket in buckets:

        print(bucket)