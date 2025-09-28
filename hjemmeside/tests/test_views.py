from django.test import TestCase, Client

# Future: are these in use?
from django.urls import reverse
from django.contrib.auth.models import User

# Future: I am importing all models, but once I've detemermined what I need changed the import to that.
from hjemmeside.models import *

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create ForeningInfo for social media links
        self.forening_info = ForeningInfo.objects.create(
            organisasjon_navn = "Bergen Parkour",
            adresse="Test Address 123",
            post_nummer="5020",
            organisasjon_nummer = "923132228",
            kontakt_tlf="12345678",
            kontakt_mail = "bergen.parkour@gmail.com",
            facebook_side = "Bergenparkour",
            instagram_side = "bergenparkour",
            om_foreningen="Test info about association",
            i_bruk=True  # Important - your function filters for this!
        )

    def assert_common_page_elements(self, response):
        """Helper method to check basic page elements"""

        required_elements =[
            # Navbar tests
            '<nav',
            'href="/instagram/"',
            'href="/facebook/"',
            'href="/kontakt/"',

            # Main content tests
            '<main',

            # Footer tests
            '<footer',
            'Bergen Parkour',
            '923132228',
            '12345678',
            'bergen.parkour@gmail.com',
            'Test Address 123',
            '5020'
        ]

        for element in required_elements:
            with self.subTest(element=element):
                self.assertContains(response, element)

    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_common_page_elements(response)

    def test_contact_loads(self):
        response = self.client.get('/kontakt/')
        self.assertEqual(response.status_code, 200)
        self.assert_common_page_elements(response)

    def test_instagram_redirect(self):
        response = self.client.get('/instagram/')
        self.assertEqual(response.status_code, 302)  # Check it's a redirect
        self.assertEqual(response.url, 'https://www.instagram.com/bergenparkour/')

    def test_facebook_redirect(self):
        response = self.client.get('/facebook/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://www.facebook.com/Bergenparkour/')

    # Future: TO test these I need a form submission so I'll wait till I get around to doing that.
    
    # def test_signup_loads(self):
    #     response = self.client.get('/pamelding')
    #     self.assertEqual(response.status_code, 200)

    # def test_signup_bekreftelse_loads(self):
    #     response = self.client.get('/bekreftelse')
    #     self.assertEqual(response.status_code, 200)

    # def test_contact_bekreftelse_loads(self):
    #     response = self.client.get('/bekreftelse')
    #     self.assertEqual(response.status_code, 200)