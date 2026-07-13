from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

from apps.clients.models import Client
from .models import Sale


class ShiftCloseViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='cajero', password='12345678')
        self.customer = Client.objects.create(
            name='Cliente Test',
            client_type='PERSON',
            identification='123456789',
            email='test@example.com',
            phone='8090000000',
            created_by=self.user,
        )

    def test_shift_close_page_shows_sales_summary(self):
        Sale.objects.create(
            client=self.customer,
            subtotal=Decimal('100.00'),
            discount=Decimal('0.00'),
            tax=Decimal('18.00'),
            tax_rate=Decimal('18.00'),
            total=Decimal('118.00'),
            payment_method='CASH',
            status='PAID',
            created_by=self.user,
        )

        self.client.force_login(self.user)
        response = self.client.get(reverse('sales:shift-close'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resumen de cierre de turno')
        self.assertContains(response, '118.00')
