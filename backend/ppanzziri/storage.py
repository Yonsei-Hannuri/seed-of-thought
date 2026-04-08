import io
import os
import uuid
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from PIL import Image


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
    if not cloudfront_base:
        raise RuntimeError('PPANZZIRI_CLOUDFRONT_URL is not configured.')
    return f"{cloudfront_base.rstrip('/')}/{object_key.lstrip('/')}"


def _extract_object_key(photo_url):
    if not photo_url:
        return ''

    cloudfront_base = _cloudfront_base_url()
    if cloudfront_base:
        prefix = f"{cloudfront_base.rstrip('/')}/"
        if photo_url.startswith(prefix):
            return photo_url[len(prefix):].lstrip('/')

    parsed = urlparse(photo_url)
    return parsed.path.lstrip('/') if parsed.scheme else photo_url.lstrip('/')


def _to_rgb(img):
    if img.mode in ('RGBA', 'P', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        return background
    if img.mode != 'RGB':
        return img.convert('RGB')
    return img


def _make_compressed(uploaded_file):
    uploaded_file.seek(0)
    img = _to_rgb(Image.open(uploaded_file))
    output = io.BytesIO()
    img.save(output, format='WEBP', quality=80)
    output.seek(0)
    return output


def _make_resized(uploaded_file):
    uploaded_file.seek(0)
    img = _to_rgb(Image.open(uploaded_file))

    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    img = img.resize((150, 150), Image.LANCZOS)

    output = io.BytesIO()
    img.save(output, format='WEBP', quality=80)
    output.seek(0)
    return output


def _get_s3_client():
    bucket = _bucket_name()
    if not bucket:
        raise RuntimeError('S3 bucket is not configured.')
    s3_client = _build_s3_client()
    if s3_client is None:
        raise RuntimeError('S3 client initialization failed.')
    return s3_client, bucket


def upload_photos(uploaded_file, namespace):
    """Upload original, compressed, and resized (150x150 WebP) versions to S3.

    Returns dict: {'original': url, 'compressed': url, 'resized': url}
    """
    if not uploaded_file:
        return {'original': '', 'compressed': '', 'resized': ''}

    extension = Path(uploaded_file.name).suffix.lower()
    base_key = f"budget/{namespace}/{datetime.now():%Y/%m}/{uuid.uuid4().hex}"
    original_key = f"{base_key}_original{extension}"
    compressed_key = f"{base_key}_compressed.webp"
    resized_key = f"{base_key}_resized.webp"

    compressed_data = _make_compressed(uploaded_file)
    resized_data = _make_resized(uploaded_file)
    uploaded_file.seek(0)

    s3_client, bucket = _get_s3_client()
    try:
        s3_client.put_object(Body=uploaded_file, Bucket=bucket, Key=original_key, ContentType=uploaded_file.content_type)
        s3_client.put_object(Body=compressed_data, Bucket=bucket, Key=compressed_key, ContentType='image/webp')
        s3_client.put_object(Body=resized_data, Bucket=bucket, Key=resized_key, ContentType='image/webp')
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError('Failed to upload file to S3.') from exc

    return {
        'original': _build_photo_url(original_key),
        'compressed': _build_photo_url(compressed_key),
        'resized': _build_photo_url(resized_key),
    }


def upload_photo_compressed(uploaded_file, namespace):
    """Upload a single WebP-compressed version to S3. Used for certifications.

    Returns compressed URL string.
    """
    if not uploaded_file:
        return ''

    base_key = f"budget/{namespace}/{datetime.now():%Y/%m}/{uuid.uuid4().hex}_compressed.webp"

    compressed_data = _make_compressed(uploaded_file)

    s3_client, bucket = _get_s3_client()
    try:
        s3_client.put_object(Body=compressed_data, Bucket=bucket, Key=base_key, ContentType='image/webp')
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError('Failed to upload file to S3.') from exc

    return _build_photo_url(base_key)


def backfill_certification_photo(photo_url):
    """Compress existing certification photo to WebP if not already converted.

    Returns new compressed URL, or original URL if already WebP.
    Temporary backfill utility.
    """
    if not photo_url or photo_url.endswith('.webp'):
        return photo_url

    object_key = _extract_object_key(photo_url)
    if not object_key:
        return photo_url

    s3_client, bucket = _get_s3_client()

    try:
        response = s3_client.get_object(Bucket=bucket, Key=object_key)
        image_data = response['Body'].read()
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError('Failed to download certification photo from S3.') from exc

    stem = str(Path(object_key).with_suffix(''))
    compressed_key = f"{stem}_compressed.webp"

    file_obj = io.BytesIO(image_data)
    compressed_data = _make_compressed(file_obj)

    try:
        s3_client.put_object(Body=compressed_data, Bucket=bucket, Key=compressed_key, ContentType='image/webp')
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError('Failed to upload compressed certification photo to S3.') from exc

    try:
        s3_client.delete_object(Bucket=bucket, Key=object_key)
    except (BotoCoreError, ClientError):
        pass

    return _build_photo_url(compressed_key)


def backfill_photo_versions(photo_url_original):
    """Rename old original (no _original suffix) in S3 and create compressed/resized versions.

    Returns (original_url, compressed_url, resized_url). Temporary backfill utility.
    """
    object_key = _extract_object_key(photo_url_original)
    if not object_key:
        return photo_url_original, '', ''

    s3_client, bucket = _get_s3_client()

    stem = str(Path(object_key).with_suffix(''))
    ext = Path(object_key).suffix

    if not stem.endswith('_original'):
        # Old file: rename to add _original suffix for consistency
        new_original_key = f"{stem}_original{ext}"
        try:
            s3_client.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': object_key},
                Key=new_original_key,
            )
            s3_client.delete_object(Bucket=bucket, Key=object_key)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError('Failed to rename original in S3.') from exc
        object_key = new_original_key
        photo_url_original = _build_photo_url(new_original_key)
    else:
        stem = stem[:-len('_original')]

    try:
        response = s3_client.get_object(Bucket=bucket, Key=object_key)
        image_data = response['Body'].read()
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError('Failed to download original from S3.') from exc

    compressed_key = f"{stem}_compressed.webp"
    resized_key = f"{stem}_resized.webp"

    file_obj = io.BytesIO(image_data)
    compressed_data = _make_compressed(file_obj)
    resized_data = _make_resized(file_obj)

    try:
        s3_client.put_object(Body=compressed_data, Bucket=bucket, Key=compressed_key, ContentType='image/webp')
        s3_client.put_object(Body=resized_data, Bucket=bucket, Key=resized_key, ContentType='image/webp')
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError('Failed to upload backfilled versions to S3.') from exc

    return photo_url_original, _build_photo_url(compressed_key), _build_photo_url(resized_key)


def delete_photo(photo_url):
    """Delete a single file from S3."""
    object_key = _extract_object_key(photo_url)
    if not object_key:
        return
    s3_client, bucket = _get_s3_client()
    try:
        s3_client.delete_object(Bucket=bucket, Key=object_key)
    except (BotoCoreError, ClientError):
        pass


def delete_photos(photo_url_original, photo_url_compressed, photo_url_resized):
    """Delete all 3 versions from S3."""
    s3_client, bucket = _get_s3_client()
    for url in [photo_url_original, photo_url_compressed, photo_url_resized]:
        object_key = _extract_object_key(url)
        if not object_key:
            continue
        try:
            s3_client.delete_object(Bucket=bucket, Key=object_key)
        except (BotoCoreError, ClientError):
            pass
