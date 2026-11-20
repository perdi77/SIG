from django.test import TestCase, Client
from django.urls import reverse

class PetaIndonesiaTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_welcome_view(self):
        response = self.client.get('/welcome/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Selamat Datang")

    def test_petasatu_view(self):
        response = self.client.get('/petasatu/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'petaindonesia/petasatu.html')
        self.assertContains(response, "Peta Indonesia")

    def test_petadua_view(self):
        response = self.client.get('/petadua/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'petaindonesia/petadua.html')
        self.assertContains(response, "Peta Jabodetabek")
