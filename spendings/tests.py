from django.contrib.auth import get_user_model
from django.test import TestCase

from spendings.serializers import ExpenseSerializer


class ExpenseSerializerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alex",
            email="alex@example.com",
            password="secret123",
        )

    def test_category_and_payment_method_are_normalized(self):
        serializer = ExpenseSerializer(
            data={
                "title": "medicine",
                "amount": "4040",
                "category": "Health",
                "payment_method": "upi",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save(owner=self.user)

        self.assertEqual(instance.category, "HEALTH")
        self.assertEqual(instance.payment_method, "upi")
