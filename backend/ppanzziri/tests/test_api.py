import os
import shutil
import tempfile
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase


class PpanzziriApiTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.temp_media_dir = tempfile.mkdtemp(prefix='ppanzziri-test-media-')
        self.override = override_settings(MEDIA_ROOT=self.temp_media_dir, MEDIA_URL='/uploads/')
        self.override.enable()
        self.env_patch = patch.dict(
            os.environ,
            {
                'PPANZZIRI_ADMIN_PASSWORD': 'secret',
                'PPANZZIRI_START_CAPITAL': '30000000',
                'PPANZZIRI_S3_BUCKET': '',
                'S3_BUCKET_NAME': '',
                'AWS_S3_BUCKET': '',
                'PPANZZIRI_CLOUDFRONT_URL': '',
                'CLOUDFRONT_URL': '',
            },
            clear=False,
        )
        self.env_patch.start()

    def tearDown(self):
        self.env_patch.stop()
        self.override.disable()
        shutil.rmtree(self.temp_media_dir, ignore_errors=True)
        super().tearDown()

    def _auth_headers(self):
        return {'HTTP_X_ADMIN_PASSWORD': 'secret'}

    def _create_record(self, **kwargs):
        payload = {
            'type': 'expense',
            'transaction_date': '2026-02-20',
            'amount': '30000',
            'memo': '감자탕',
            'effective_segments': (
                '[{"effective_from":"2026-02-20","effective_to":"2026-02-21","segment_amount":15000},'
                '{"effective_from":"2026-02-22","effective_to":"2026-02-22","segment_amount":15000}]'
            ),
            'tags': '["생활비", "경험소비"]',
        }
        payload.update(kwargs)
        return self.client.post('/ppanzziri/budget/records', payload, **self._auth_headers())

    def test_create_record_and_read_dashboard(self):
        response = self._create_record()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['amount'], 30000)
        self.assertEqual(response.data['memo'], '감자탕')
        self.assertRegex(response.data['created_at'], r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$')
        self.assertEqual(len(response.data['effective_segments']), 2)
        self.assertEqual(sum(tag['amount'] for tag in response.data['tags']), 30000)

        dashboard_response = self.client.get('/ppanzziri/dashboard')
        self.assertEqual(dashboard_response.status_code, status.HTTP_200_OK)
        self.assertEqual(dashboard_response.data['startCapital'], 30000000)
        self.assertEqual(dashboard_response.data['totalExpense'], 30000)
        self.assertEqual(dashboard_response.data['totalIncome'], 0)
        self.assertEqual(dashboard_response.data['currentBalance'], 29970000)
        self.assertEqual(len(dashboard_response.data['records']), 1)
        self.assertEqual(dashboard_response.data['records'][0]['memo'], '감자탕')
        self.assertEqual(dashboard_response.data['certifications'], [])
        self.assertIn('social', dashboard_response.data)

    def test_create_record_without_segments_uses_default_segment(self):
        response = self._create_record(effective_segments='')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['effective_segments']), 1)
        self.assertEqual(response.data['effective_segments'][0]['segment_amount'], 30000)

    def test_create_record_rejects_invalid_segment_sum(self):
        response = self._create_record(
            effective_segments=(
                '[{"effective_from":"2026-02-20","effective_to":"2026-02-20","segment_amount":10000}]'
            )
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('effective_segments', response.data)

    def test_create_record_rejects_invalid_tag_sum_when_amounts_provided(self):
        response = self._create_record(
            tags='[{"name":"생활비","amount":10000},{"name":"경험소비","amount":5000}]'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tags', response.data)

    def test_post_requires_admin_password_when_configured(self):
        response = self.client.post(
            '/ppanzziri/budget/records',
            {
                'type': 'income',
                'transaction_date': '2026-02-20',
                'amount': '10000',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_budget_records_and_delete_record(self):
        create_response = self._create_record()
        record_id = create_response.data['id']

        list_response = self.client.get('/ppanzziri/budget/records')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        delete_response = self.client.delete(
            f'/ppanzziri/budget/records/{record_id}',
            **self._auth_headers(),
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        empty_list_response = self.client.get('/ppanzziri/budget/records')
        self.assertEqual(empty_list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(empty_list_response.data, [])

    def test_budget_tags_aggregates_amounts(self):
        self._create_record(tags='[{"name":"생활비","amount":20000},{"name":"경험소비","amount":10000}]')
        self._create_record(
            type='income',
            amount='10000',
            effective_segments='[{"effective_from":"2026-02-21","effective_to":"2026-02-21","segment_amount":10000}]',
            tags='["생활비"]',
        )
        self._create_record(
            type='income',
            amount='7000',
            effective_segments='[{"effective_from":"2026-02-22","effective_to":"2026-02-22","segment_amount":7000}]',
            tags='["월급"]',
        )

        tags_response = self.client.get('/ppanzziri/budget/tags')
        self.assertEqual(tags_response.status_code, status.HTTP_200_OK)
        by_key = {(item['name'], item['recordType']): item for item in tags_response.data}

        self.assertEqual(by_key[('생활비', 'EXPENSE')]['amount'], 20000)
        self.assertEqual(by_key[('생활비', 'INCOME')]['amount'], 10000)
        self.assertEqual(by_key[('경험소비', 'EXPENSE')]['amount'], 10000)
        self.assertEqual(by_key[('월급', 'INCOME')]['amount'], 7000)

    def test_create_list_replace_and_delete_certification(self):
        file1 = SimpleUploadedFile('proof1.jpg', b'fake-image-content-1', content_type='image/jpeg')
        file2 = SimpleUploadedFile('proof2.jpg', b'fake-image-content-2', content_type='image/jpeg')

        create_response = self.client.post(
            '/ppanzziri/budget/certifications',
            {'date': '2026-02-21', 'photo': file1},
            format='multipart',
            **self._auth_headers(),
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        first_photo_url = create_response.data['photo_url']

        replace_response = self.client.post(
            '/ppanzziri/budget/certifications',
            {'date': '2026-02-21', 'photo': file2},
            format='multipart',
            **self._auth_headers(),
        )
        self.assertEqual(replace_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(replace_response.data['photo_url'], first_photo_url)

        list_response = self.client.get('/ppanzziri/budget/certifications')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        delete_response = self.client.delete(
            '/ppanzziri/budget/certifications/2026-02-21',
            **self._auth_headers(),
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_certification_requires_admin_password(self):
        response = self.client.delete('/ppanzziri/budget/certifications/2026-02-21')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_social_default(self):
        response = self.client.get('/ppanzziri/social')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'youtube_embed_url': '',
                'instagram_post_url': '',
                'instagram_profile_url': '',
                'extra_links': [],
            },
        )

    def test_put_social_and_dashboard_snapshot(self):
        response = self.client.put(
            '/ppanzziri/social',
            {
                'youtube_embed_url': ' https://www.youtube.com/embed/abc123?foo=bar ',
                'instagram_post_url': 'https://www.instagram.com/p/C9AbCdEf/?utm=1',
                'instagram_profile_url': ' https://www.instagram.com/ppanzziri ',
                'extra_links': [
                    {'label': '  블로그  ', 'href': '  https://example.com/a?b=1  '},
                    {'label': ' ', 'href': ' '},
                ],
            },
            format='json',
            **self._auth_headers(),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'ok': True})

        social_response = self.client.get('/ppanzziri/social')
        self.assertEqual(social_response.status_code, status.HTTP_200_OK)
        self.assertEqual(social_response.data['youtube_embed_url'], 'https://www.youtube.com/embed/abc123')
        self.assertEqual(social_response.data['instagram_post_url'], 'https://www.instagram.com/p/C9AbCdEf/')
        self.assertEqual(social_response.data['instagram_profile_url'], 'https://www.instagram.com/ppanzziri/')
        self.assertEqual(
            social_response.data['extra_links'],
            [{'label': '블로그', 'href': 'https://example.com/a?b=1'}],
        )

        dashboard_response = self.client.get('/ppanzziri/dashboard')
        self.assertEqual(dashboard_response.status_code, status.HTTP_200_OK)
        self.assertEqual(dashboard_response.data['social'], social_response.data)

    def test_put_social_requires_admin_password(self):
        response = self.client.put('/ppanzziri/social', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_social_rejects_invalid_values(self):
        response = self.client.put(
            '/ppanzziri/social',
            {
                'youtube_embed_url': 'http://www.youtube.com/embed/abc123',
                'instagram_post_url': 'https://www.instagram.com/reel/xxxx/',
                'instagram_profile_url': 'https://www.instagram.com/p/xxxx/',
                'extra_links': [{'label': '링크', 'href': 'ftp://example.com'}] * 7,
            },
            format='json',
            **self._auth_headers(),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
