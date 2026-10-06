from flask import Flask, jsonify, request
from flask_cors import CORS

from s3_service import (
    list_buckets,
    create_bucket,
    upload_file,
    list_files,
    download_file,
    delete_file
)

from ec2_service import (
    list_instances,
    launch_instance,
    start_instance,
    stop_instance,
    terminate_instance
)


app = Flask(__name__)

CORS(app)


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return jsonify({
        "message": "AWS Automation Dashboard API is running!"
    })


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "service": "AWS Automation Backend"
    })


# ==========================================
# S3 - LIST BUCKETS
# ==========================================

@app.route("/s3/buckets", methods=["GET"])
def get_buckets():

    try:

        buckets = list_buckets()

        return jsonify({
            "success": True,
            "buckets": buckets
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# S3 - CREATE BUCKET
# ==========================================

@app.route("/s3/buckets", methods=["POST"])
def add_bucket():

    data = request.get_json()

    bucket_name = data.get("bucket_name")

    if not bucket_name:

        return jsonify({
            "success": False,
            "error": "Bucket name is required"
        }), 400

    try:

        create_bucket(bucket_name)

        return jsonify({
            "success": True,
            "message": "Bucket created successfully!"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# S3 - LIST FILES
# ==========================================

@app.route("/s3/files", methods=["GET"])
def get_files():

    bucket_name = request.args.get("bucket")

    if not bucket_name:

        return jsonify({
            "success": False,
            "error": "Bucket name is required"
        }), 400

    try:

        files = list_files(bucket_name)

        return jsonify({
            "success": True,
            "files": files
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# S3 - UPLOAD FILE
# ==========================================

@app.route("/s3/upload", methods=["POST"])
def upload():

    file = request.files.get("file")
    bucket_name = request.form.get("bucket_name")

    if not file:

        return jsonify({
            "success": False,
            "error": "File is required"
        }), 400

    if not bucket_name:

        return jsonify({
            "success": False,
            "error": "Bucket name is required"
        }), 400

    try:

        upload_file(
            file,
            bucket_name,
            file.filename
        )

        return jsonify({
            "success": True,
            "message": "File uploaded successfully!"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# S3 - DOWNLOAD FILE
# ==========================================

@app.route("/s3/download", methods=["GET"])
def download():

    bucket_name = request.args.get("bucket")
    object_name = request.args.get("file")

    if not bucket_name or not object_name:

        return jsonify({
            "success": False,
            "error": "Bucket and file are required"
        }), 400

    try:

        download_path = object_name

        download_file(
            bucket_name,
            object_name,
            download_path
        )

        return jsonify({
            "success": True,
            "message": "File downloaded successfully!",
            "file": download_path
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# S3 - DELETE FILE
# ==========================================

@app.route("/s3/delete", methods=["DELETE"])
def delete():

    data = request.get_json()

    bucket_name = data.get("bucket")
    object_name = data.get("file")

    if not bucket_name or not object_name:

        return jsonify({
            "success": False,
            "error": "Bucket and file are required"
        }), 400

    try:

        delete_file(
            bucket_name,
            object_name
        )

        return jsonify({
            "success": True,
            "message": "File deleted successfully!"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# EC2 - LAUNCH INSTANCE
# ==========================================

@app.route(
    "/ec2/launch",
    methods=["POST"]
)
def launch_ec2():

    data = request.get_json()

    instance_name = data.get("instance_name")

    if not instance_name:

        return jsonify({
            "success": False,
            "error": "Instance name is required"
        }), 400

    try:

        instance_id = launch_instance(
            instance_name
        )

        return jsonify({
            "success": True,
            "message": "EC2 instance launched successfully!",
            "instance_id": instance_id
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# EC2 - LIST INSTANCES
# ==========================================

@app.route("/ec2/instances", methods=["GET"])
def get_instances():

    try:

        instances = list_instances()

        return jsonify({
            "success": True,
            "instances": instances
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# EC2 - START INSTANCE
# ==========================================

@app.route(
    "/ec2/start/<instance_id>",
    methods=["POST"]
)
def start_ec2(instance_id):

    try:

        start_instance(instance_id)

        return jsonify({
            "success": True,
            "message": "EC2 instance start command sent successfully!"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# EC2 - STOP INSTANCE
# ==========================================

@app.route(
    "/ec2/stop/<instance_id>",
    methods=["POST"]
)
def stop_ec2(instance_id):

    try:

        stop_instance(instance_id)

        return jsonify({
            "success": True,
            "message": "EC2 instance stop command sent successfully!"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# EC2 - TERMINATE INSTANCE
# ==========================================

@app.route(
    "/ec2/terminate/<instance_id>",
    methods=["POST"]
)
def terminate_ec2(instance_id):

    try:

        terminate_instance(instance_id)

        return jsonify({
            "success": True,
            "message": "EC2 instance termination command sent successfully!"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# RUN FLASK SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )