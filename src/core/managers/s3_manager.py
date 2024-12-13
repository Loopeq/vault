from contextlib import asynccontextmanager
from fastapi import UploadFile
from core.logger import logging
from core.settings import settings
from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session

logger = logging.getLogger(__name__)


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self) -> AioBaseClient:
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
        self,
        file: UploadFile,
        user_uuid: str,
        file_uuid: str,
    ):
        async with self.get_client() as client:
            content = await file.read()
            await client.put_object(
                Bucket=self.bucket_name,
                Key=f"{user_uuid}/{file_uuid}",
                Body=content,
            )

    async def get_file(self, user_uuid: str, file_uuid: str):
        async with self.get_client() as client:
            response = await client.get_object(
                Bucket=self.bucket_name, Key=f"{user_uuid}/{file_uuid}"
            )

            content = await response["Body"].read()
            return content


s3_manager = S3Client(
    access_key=settings.s3.access_key,
    secret_key=settings.s3.secret_key,
    endpoint_url=settings.s3.url,
    bucket_name=settings.s3.bucket,
)
