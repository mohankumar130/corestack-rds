import boto3
import sys
import json

def get_rds_status(client, rds_instance_id):
    """Check the current status of the RDS instance."""
    try:
        response = client.describe_db_instances(DBInstanceIdentifier=rds_instance_id)
        status = response["DBInstances"][0]["DBInstanceStatus"]
        return status
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

def stop_rds(region, rds_instance_id):
    """Stop the RDS instance if it is available."""
    client = boto3.client("rds", region_name=region)
    
    # Get current state
    current_state = get_rds_status(client, rds_instance_id)

    if current_state == "available":
        try:
            client.stop_db_instance(DBInstanceIdentifier=rds_instance_id)
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
    
    # Get updated state
    new_state = get_rds_status(client, rds_instance_id)

    # Print output in JSON format for Terraform to read
    print(json.dumps({"current_state": current_state, "new_state": new_state}))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Usage: stop_rds.py <aws_region> <rds_instance_id>"}))
        sys.exit(1)

    region = sys.argv[1]
    rds_instance_id = sys.argv[2]

    stop_rds(region, rds_instance_id)
