# Fetch current RDS state before making changes
data "external" "rds_status" {
  program = ["python3", "get_rds_status.py", var.aws_region, var.rds_instance_id]
}

output "rds_current_state" {
  value = data.external.rds_status.result["current_state"]
}

# Stop RDS if it's running
resource "null_resource" "stop_rds" {
  count = data.external.rds_status.result["current_state"] == "available" ? 1 : 0

  provisioner "local-exec" {
    interpreter = ["bash", "-c"]
    command = <<EOT
      #!/bin/bash
      curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py
      python3 get-pip.py
      python3 -m pip install boto3

      # Run script in background and detach (immediate Terraform completion)
      nohup python3 stop_rds.py ${var.aws_region} ${var.rds_instance_id}
    EOT
  }

  triggers = {
    always_run = "${uuid()}"
  }
}

# Fetch new RDS state after stopping
data "external" "rds_new_status" {
  depends_on = [null_resource.stop_rds]
  program = ["python3", "get_rds_status.py", var.aws_region, var.rds_instance_id]
}

output "rds_new_state" {
  value = data.external.rds_new_status.result["current_state"]
}
