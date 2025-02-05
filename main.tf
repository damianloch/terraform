provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0"  # Use a valid AMI
  instance_type = "t2.micro"
  key_name      = "my-key"  # Replace with your SSH key name
  user_data     = file("install.sh")

  tags = {
    Name = "SimpleTerraformApp"
  }
}

output "public_ip" {
  value = aws_instance.app_server.public_ip
}
