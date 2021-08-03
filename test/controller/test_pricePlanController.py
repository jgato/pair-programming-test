import unittest

from repository.price_plan_repository import price_plan_repository
from app_initializer import initialize_data


from .setup_test_app import app

class TestPricePlanController(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        initialize_data()

    def tearDown(self):
        price_plan_repository.clear()

    def test_get_all_price_plans(self):
        res = self.client.get('/price-plans/')
        self.assertEqual(res.status_code, 200)
        plans = res.get_json()
        self.assertIn('price-plan-0',plans)
        self.assertIn('price-plan-1',plans)
        self.assertIn('price-plan-2',plans)
        self.assertEqual(plans['price-plan-0']['name'], 'price-plan-0')
        self.assertEqual(plans['price-plan-0'], {
                    'name': 'price-plan-0',
                    'supplier': "Dr Evil's Dark Energy",
                    'unit_rate': 10,
                    'peak_time_multiplier': []
                })
        self.assertEqual(plans, 
            {
                'price-plan-0': {
                    'name': 'price-plan-0',
                    'supplier': "Dr Evil's Dark Energy",
                    'unit_rate': 10,
                    'peak_time_multiplier': []
                },
                'price-plan-1': {
                    'name': 'price-plan-1',
                    'supplier': 'The Green Eco',
                    'unit_rate': 2,
                    'peak_time_multiplier': []
                },
                'price-plan-2': {
                    'name': 'price-plan-2',
                    'supplier': 'Power for Everyone',
                    'unit_rate': 1,
                    'peak_time_multiplier': []
                }
            }
        )
        # self.assertEqual(res.get_json()['pricePlanId'], 'price-plan-1')
        # self.assertEqual(len(res.get_json()['pricePlanComparisons']), 3)