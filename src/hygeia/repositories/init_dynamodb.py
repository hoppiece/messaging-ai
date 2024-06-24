import boto3
from hygeia.botconf import dynamodb
from hygeia.config import settings


def create_table_dynamodb_local() -> None:
    table = dynamodb.create_table(
        TableName="hygeia-user",
        KeySchema=[
            {
                "AttributeName": "user_id",
                "KeyType": "HASH",  # パーティションキー
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "user_id",
                "AttributeType": "S",  # String
            }
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
    table.wait_until_exists()
    print(f"Table {table.table_name} created successfully.")


if __name__ == "__main__":
    create_table_dynamodb_local()
