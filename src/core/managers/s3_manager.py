from contextlib import asynccontextmanager
from core.settings import settings
from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session


class S3Client:
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 endpoint_url: str,
                 bucket_name: str):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_key_id": secret_key,
            "endpoint_url": endpoint_url
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self) -> AioBaseClient:
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self,
                          file_path: str):
        object_name = file_path.split('/')[-1]
        async with self.get_client() as client:
            with open(file_path, "rb") as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file
                )


s3_manager = S3Client(
    access_key=settings.s3.access_key,
    secret_key=settings.s3.secret_key,
    endpoint_url=settings.s3.url,
    bucket_name=settings.s3.bucket
)

