resource "null_resource" "stop_rds_instance" {
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    interpreter = ["bash", "-c"]
    command = <<-EOF
    #!/bin/bash
    curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    python3 -m pip install boto3

    # Run Python script to stop RDS
    python3 stop_rds.py ${var.rds_instance_name} ${var.aws_region}

    # Save the status file for Terraform
    cp rds_status.txt terraform_rds_status.txt
    EOF
  }
}

resource "local_file" "rds_status" {
  content  = file("terraform_rds_status.txt")
  filename = "${path.module}/terraform_rds_status.txt"
}

output "rds_stop_status" {
  value = local_file.rds_status.content
}
