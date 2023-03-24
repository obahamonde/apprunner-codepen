import json
import base64
import boto3
from functools import wraps
from httpx import AsyncClient
from botocore.exceptions import ClientError
from fastapi import File, UploadFile
from redis import Redis
from src.config import env

store = Redis(
    host=env.REDIS_HOST,
    port=env.REDIS_PORT,
    password=env.REDIS_PASSWORD,
    username="default",
    decode_responses=True,
    encoding="utf-8",
)


def cache(ttl: int = 3600):
    """Cache decorator."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = base64.b64encode(
                f"{func.__name__}{args}{kwargs}".encode("utf-8")
            ).decode("utf-8")
            value = store.get(key)
            if value:
                return json.loads(value)
            else:
                value = func(*args, **kwargs)
                store.set(key, str(value), ex=ttl)
                return value

        return wrapper

    return decorator

def async_cache(ttl: int = 3600):
    """Async cache decorator."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = base64.b64encode(
                f"{func.__name__}{args}{kwargs}".encode("utf-8")
            ).decode("utf-8")
            value = store.get(key)
            if value:
                return json.loads(value)
            else:
                value = await func(*args, **kwargs)
                store.set(key, json.dumps(value), ex=ttl)
                return value

        return wrapper

    return decorator



class S3Service:
    """S3 service."""

    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=env.AWS_S3_ENDPOINT,
            aws_access_key_id=env.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
            region_name="us-east-1",
            config=boto3.session.Config(signature_version="s3v4")
        )
        
    @cache()
    def get_url(self, key: str) -> str:
        """Get file url."""
        return self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": env.AWS_S3_BUCKET, "Key": key},
            ExpiresIn=3600,
        )
        
        
    def upload_file(self, key: str, file: bytes) -> str:
        """Upload file."""
        try:
            self.s3.put_object(
                Bucket=env.AWS_S3_BUCKET,
                Key=f"{key}.html",
                Body=file,
                ContentType="text/html",
                ACL="public-read"
            )
            
        except ClientError as e:
            print(e)
            return "Error uploading file."


    def delete_file(self, key: str) -> str:
        """Delete file."""
        try:
            self.s3.delete_object(Bucket=env.AWS_S3_BUCKET, Key=key)
            return "File deleted."
        except ClientError as e:
            print(e)
            return "Error deleting file."


class AuthService:
    """Auth service."""

    def __init__(self):
        self.url = f"https://dev-tvhqmk7a.us.auth0.com/userinfo"

    @async_cache()
    async def get_user(self, token: str) -> dict:
        async with AsyncClient() as client:
            response = await client.get(
                self.url, headers={"Authorization": f"Bearer {token}"}
            )
            return response.json()


  