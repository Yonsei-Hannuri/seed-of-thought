import io

from botocore.exceptions import BotoCoreError, ClientError
from django.core.management.base import BaseCommand

from ppanzziri.models import BudgetRecord
from ppanzziri.storage import (
    _extract_object_key,
    _get_s3_client,
    _make_compressed,
    _make_resized,
)


class Command(BaseCommand):
    help = 'S3의 compressed/resized 이미지를 삭제하고 원본에서 재생성합니다 (EXIF 회전 보정)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='실제 변경 없이 처리 대상만 출력',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        s3_client, bucket = _get_s3_client()

        records = BudgetRecord.objects.exclude(photo_url_original='')
        total = records.count()
        self.stdout.write(f'처리 대상: {total}건')

        ok = 0
        skipped = 0
        failed = 0

        for record in records:
            original_key = _extract_object_key(record.photo_url_original)
            compressed_key = _extract_object_key(record.photo_url_compressed)
            resized_key = _extract_object_key(record.photo_url_resized)

            if not original_key:
                self.stdout.write(self.style.WARNING(f'  [{record.id}] original URL 없음 — 스킵'))
                skipped += 1
                continue

            if dry_run:
                self.stdout.write(f'  [{record.id}] {original_key}')
                continue

            # 1. 원본 다운로드
            try:
                response = s3_client.get_object(Bucket=bucket, Key=original_key)
                image_data = response['Body'].read()
            except (BotoCoreError, ClientError) as e:
                self.stdout.write(self.style.ERROR(f'  [{record.id}] 원본 다운로드 실패: {e}'))
                failed += 1
                continue

            file_obj = io.BytesIO(image_data)

            # 2. compressed/resized 재생성
            try:
                compressed_data = _make_compressed(file_obj)
                resized_data = _make_resized(file_obj)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [{record.id}] 이미지 처리 실패: {e}'))
                failed += 1
                continue

            # 3. 기존 S3 객체 삭제 후 재업로드
            try:
                for key in [compressed_key, resized_key]:
                    if key:
                        s3_client.delete_object(Bucket=bucket, Key=key)

                if compressed_key:
                    s3_client.put_object(
                        Body=compressed_data,
                        Bucket=bucket,
                        Key=compressed_key,
                        ContentType='image/webp',
                    )
                if resized_key:
                    s3_client.put_object(
                        Body=resized_data,
                        Bucket=bucket,
                        Key=resized_key,
                        ContentType='image/webp',
                    )
            except (BotoCoreError, ClientError) as e:
                self.stdout.write(self.style.ERROR(f'  [{record.id}] S3 업로드 실패: {e}'))
                failed += 1
                continue

            self.stdout.write(self.style.SUCCESS(f'  [{record.id}] 완료'))
            ok += 1

        self.stdout.write(f'\n완료: {ok} / 스킵: {skipped} / 실패: {failed}')
