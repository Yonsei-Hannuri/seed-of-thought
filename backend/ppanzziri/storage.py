import os
import uuid
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from django.conf import settings


def _cloudfront_base_url():
    return (
        os.getenv('PPANZZIRI_CLOUDFRONT_URL')
        or os.getenv('CLOUDFRONT_URL')
        or ''
    ).strip()


def _bucket_name():
    return (
        os.getenv('PPANZZIRI_S3_BUCKET')
        or os.getenv('S3_BUCKET_NAME')
        or os.getenv('AWS_S3_BUCKET')
        or ''
    ).strip()


def _build_s3_client():
    region = (
        os.getenv('PPANZZIRI_AWS_REGION')
        or os.getenv('AWS_REGION')
        or os.getenv('AWS_DEFAULT_REGION')
        or None
    )
    access_key = os.getenv('PPANZZIRI_AWS_ACCESS_KEY_ID') or os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('PPANZZIRI_AWS_SECRET_ACCESS_KEY') or os.getenv('AWS_SECRET_ACCESS_KEY')

    kwargs = {}
    if region:
        kwargs['region_name'] = region
    if access_key and secret_key:
        kwargs['aws_access_key_id'] = access_key
        kwargs['aws_secret_access_key'] = secret_key

    try:
        return boto3.client('s3', **kwargs)
    except Exception:
        return None


def _build_photo_url(object_key):
    cloudfront_base = _cloudfront_base_url()
    if cloudfront_base:
        return f"{cloudfront_base.rstrip('/')}/{object_key.lstrip('/')}"
    return f"{settings.MEDIA_URL.rstrip('/')}/{object_key.lstrip('/')}"


def _extract_object_key(photo_url):
    if not photo_url:
        return ''

    cloudfront_base = _cloudfront_base_url()
    if cloudfront_base:
        prefix = f"{cloudfront_base.rstrip('/')}/"
        if photo_url.startswith(prefix):
            return photo_url[len(prefix):].lstrip('/')

    parsed = urlparse(photo_url)
    path = parsed.path.lstrip('/') if parsed.scheme else photo_url.lstrip('/')

    media_prefix = settings.MEDIA_URL.lstrip('/').rstrip('/') + '/'
    if path.startswith(media_prefix):
        return path[len(media_prefix):]

    return path


def upload_photo(uploaded_file, namespace):
    if not uploaded_file:
        return ''

    extension = Path(uploaded_file.name).suffix.lower()
    object_key = f"budget/{namespace}/{datetime.now():%Y/%m}/{uuid.uuid4().hex}{extension}"

    bucket = _bucket_name()
    if bucket:
        s3_client = _build_s3_client()
        if s3_client is None:
            raise RuntimeError('S3 client initialization failed.')
        try:
            s3_client.put_object(
                Body=uploaded_file,
                Bucket=bucket,
                Key=object_key,
                ContentType=uploaded_file.content_type,
            )
            return _build_photo_url(object_key)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError('Failed to upload file to S3.') from exc

    file_path = Path(settings.MEDIA_ROOT) / object_key
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return _build_photo_url(object_key)


def delete_photo(photo_url):
    object_key = _extract_object_key(photo_url)
    if not object_key:
        return

    bucket = _bucket_name()
    if bucket:
        s3_client = _build_s3_client()
        if s3_client is not None:
            try:
                s3_client.delete_object(Bucket=bucket, Key=object_key)
            except (BotoCoreError, ClientError):
                pass
        return

    file_path = Path(settings.MEDIA_ROOT) / object_key
    if file_path.exists() and file_path.is_file():
        file_path.unlink()
