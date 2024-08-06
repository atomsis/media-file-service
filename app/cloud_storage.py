import os

import aioboto3
import aiofiles
from botocore.exceptions import ClientError

class S3Client:
    def __init__(
            self,
            access_key: str,

            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'endpoint_url': endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = aioboto3.Session()

    async def upload_file(self, file_path: str):
        object_name = file_path.split('/')[-1]

        try:
            async with self.session.client('s3', **self.config) as client:
                with open(file_path, 'rb') as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file
                    )
        except ClientError as e:
            print(f"Failed to upload {file_path} to S3: {e}")
            raise

    async def download_file(self, object_name: str, file_path: str):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            async with self.session.client('s3', **self.config) as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                async with aiofiles.open(file_path, 'wb') as file:
                    content = await response['Body'].read()
                    await file.write(content)
        except ClientError as e:
            print(f"Failed to download {object_name} from S3: {e}")
            raise

