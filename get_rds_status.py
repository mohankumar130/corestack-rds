import boto3
import sys
import time

def get_rds_status(instance_id, region):
    """Check the current state of the RDS instance."""
    rds = boto3.client('rds', region_name=region)
    try:
        response = rds.describe_db_instances(DBInstanceIdentifier=instance_id)
        return response['DBInstances'][0]['DBInstanceStatus']
    except Exception as e:
        return f"❌ Error checking RDS status: {str(e)}"

def stop_rds(instance_id, region):
    """Stop the RDS instance if it's running and return final status."""
    rds = boto3.client('rds', region_name=region)

    # Get initial status
    initial_status = get_rds_status(instance_id, region)
    print(f"🔍 Initial RDS State: {initial_status}")

    if initial_status == "stopped":
        message = f"✅ RDS instance {instance_id} is already stopped."
    elif initial_status != "available":
        message = f"⚠️ RDS instance {instance_id} is in '{initial_status}' state and cannot be stopped."
    else:
        try:
            rds.stop_db_instance(DBInstanceIdentifier=instance_id)
            print(f"🛑 Stopping RDS instance: {instance_id}...")

            # Wait for instance to stop
            while True:
                time.sleep(10)  # Wait for 10 seconds before checking again
                current_status = get_rds_status(instance_id, region)
                print(f"⏳ Current RDS State: {current_status}")
                if current_status == "stopped":
                    break

            message = f"✅ Successfully stopped RDS instance {instance_id}."
        except Exception as e:
            message = f"❌ Error stopping RDS instance {instance_id}: {str(e)}"

    # Write the status to a file so Terraform can read it
    with open("rds_status.txt", "w") as f:
        f.write(message)

    print(message)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 stop_rds.py <rds_instance_id> <aws_region>")
        sys.exit(1)

    instance_id = sys.argv[1]
    region = sys.argv[2]
    stop_rds(instance_id, region)
