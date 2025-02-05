Terrraform autodeployment

$ python -m venv venv
$ venv\Scripts\activate # Windows
$ pip install -r backend/requirements.txt

# Terraform Python App Deployment

## Overview

This repository contains a minimal Terraform setup to provision an **AWS EC2 instance** and deploy a simple **Python HTTP server**.

Terraform will:

1. Create an AWS EC2 instance.
2. Run a Python application that serves a basic HTTP response.

## Prerequisites

Before running this setup, ensure you have the following installed:

- [Terraform](https://developer.hashicorp.com/terraform/downloads) (>= 1.6.x)
- [AWS CLI](https://aws.amazon.com/cli/) (Configured with credentials)
- An existing **AWS EC2 Key Pair** (for SSH access)
- Python 3 (installed on the local machine if needed for testing)

## File Structure

```
terraform-python-app/
│── app.py                    # Simple Python HTTP server
│── install.sh                 # EC2 setup script
│── main.tf                    # Terraform configuration
│── .gitignore
│── README.md
```

## How It Works

1. **Terraform provisions an EC2 instance**
2. **A startup script (`install.sh`) installs Python and runs the Python HTTP server**
3. **The Python server listens on port `8000` and returns a simple text response**
4. **You access the server via the public IP of the EC2 instance**

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/your-repo/terraform-python-app.git
cd terraform-python-app
```

### 2. Initialize Terraform

```sh
terraform init
```

This initializes Terraform and downloads necessary providers.

### 3. Apply Terraform Configuration

```sh
terraform apply -auto-approve
```

Terraform will create the EC2 instance and automatically execute the installation script.

### 4. Get the Public IP

After Terraform applies the configuration, it will output the public IP of the instance. Copy the IP and visit:

```
http://<PUBLIC_IP>:8000
```

You should see:

```
Hello from Terraform-provisioned EC2!
```

### 5. Destroy the Infrastructure

To remove the EC2 instance when you're done, run:

```sh
terraform destroy -auto-approve
```

## Breakdown of Files

### **1. `app.py`**

This is a simple HTTP server using Python's built-in `http.server` module.

```python
from http.server import SimpleHTTPRequestHandler, HTTPServer
PORT = 8000
class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from Terraform-provisioned EC2!")
server = HTTPServer(("0.0.0.0", PORT), MyHandler)
print(f"Serving on port {PORT}")
server.serve_forever()
```

### **2. `install.sh`**

This script installs Python and runs the Python app on the EC2 instance.

```sh
#!/bin/bash
sudo apt update -y
sudo apt install python3 -y
nohup python3 /home/ubuntu/app.py > /home/ubuntu/app.log 2>&1 &
```

### **3. `main.tf` (Terraform Configuration)**

Defines the AWS provider and provisions an EC2 instance with the `install.sh` script.

```hcl
provider "aws" {
  region = "us-east-1"
}
resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0"  # Replace with a valid AMI
  instance_type = "t2.micro"
  key_name      = "my-key"  # Replace with your key name
  user_data     = file("install.sh")
  tags = {
    Name = "SimpleTerraformApp"
  }
}
output "public_ip" {
  value = aws_instance.app_server.public_ip
}
```

## Troubleshooting

### **1. Terraform apply fails**

- Ensure your AWS CLI is configured: `aws configure`
- Make sure you have an active AWS account with permissions to create EC2 instances.
- Check the **AMI ID** (replace it with a valid one for your region).

### **2. Can't access the app**

- Check if the security group allows inbound traffic on port 8000.
- SSH into the instance and manually run `python3 /home/ubuntu/app.py` to debug.

## Next Steps

- Use a **remote backend** (like AWS S3) for state management.
- Attach an **Elastic IP** to keep the instance's IP address persistent.
- Deploy with **AWS Lambda + API Gateway** instead of EC2 for a serverless approach.
