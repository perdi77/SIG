import json
from django.test import TestCase, Client
from gempabumi.views import get_kedalaman_info

class GempaBumiTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_kedalaman_info_dangkal(self):
        info = get_kedalaman_info("10 km")
        self.assertEqual(info["kategori"], "dangkal")
        self.assertEqual(info["warna"], "#e53935")

        info_69 = get_kedalaman_info("69 km")
        self.assertEqual(info_69["kategori"], "dangkal")

    def test_kedalaman_info_menengah(self):
        info = get_kedalaman_info("84 km")
        self.assertEqual(info["kategori"], "menengah")
        self.assertEqual(info["warna"], "#f59e0b")

        info_300 = get_kedalaman_info("300 km")
        self.assertEqual(info_300["kategori"], "menengah")

    def test_kedalaman_info_dalam(self):
        info = get_kedalaman_info("323 km")
        self.assertEqual(info["kategori"], "dalam")
        self.assertEqual(info["warna"], "#10b981")

        info_465 = get_kedalaman_info("465 km")
        self.assertEqual(info_465["kategori"], "dalam")

    def test_gempaterkini_view(self):
        response = self.client.get('/gempabumi/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gempabumi/gempaterkini.html')
        self.assertIn('gempa_list', response.context)
        self.assertIn('total_gempa', response.context)
        self.assertIn('waktu_update', response.context)
        self.assertContains(response, "15 Gempa Terkini (M 5.0+)")
