const API_URL = "http://127.0.0.1:5000";


// ===============================
// Load S3 Bucket Count
// ===============================

async function loadBucketCount() {

    const bucketElement = document.getElementById("bucketCount");

    if (!bucketElement) {
        return;
    }

    try {

        const response = await fetch(`${API_URL}/s3/buckets`);

        const data = await response.json();

        if (data.success) {

            bucketElement.textContent =
                `${data.buckets.length} bucket(s)`;

        } else {

            bucketElement.textContent = "Unable to load";

        }

    } catch (error) {

        console.error("S3 Error:", error);

        bucketElement.textContent =
            "Backend offline";

    }
}


// ===============================
// Load EC2 Instance Count
// ===============================

async function loadInstanceCount() {

    const instanceElement =
        document.getElementById("instanceCount");

    if (!instanceElement) {
        return;
    }

    try {

        const response =
            await fetch(`${API_URL}/ec2/instances`);

        const data = await response.json();

        if (data.success) {

            instanceElement.textContent =
                `${data.instances.length} instance(s)`;

        } else {

            instanceElement.textContent =
                "Unable to load";

        }

    } catch (error) {

        console.error("EC2 Error:", error);

        instanceElement.textContent =
            "Backend offline";

    }
}


// ===============================
// Load Dashboard Data
// ===============================

async function loadDashboardData() {

    await loadBucketCount();

    await loadInstanceCount();

}


// Run when page loads

document.addEventListener(
    "DOMContentLoaded",
    loadDashboardData
);
