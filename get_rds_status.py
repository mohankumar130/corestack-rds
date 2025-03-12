import boto3
import sys
import json

def get_rds_status(region, rds_instance_id):
    """Fetch current RDS instance status."""
    client = boto3.client("rds", region_name=region)
    
    try:
        response = client.describe_db_instances(DBInstanceIdentifier=rds_instance_id)
        state = response["DBInstances"][0]["DBInstanceStatus"]
        return {"current_state": state}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Usage: get_rds_status.py <aws_region> <rds_instance_id>"}))
        sys.exit(1)

    region = sys.argv[1]
    rds_instance_id = sys.argv[2]

    print(json.dumps(get_rds_status(region, rds_instance_id)))
