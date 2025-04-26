from django.test import TestCase
from django.urls import reverse
from .utils import evaluate_and_store_result, parse_timestamp, evaluate_expression
from .models import KPI, KPIAssetLink, EvaluationResult


class EvaluateExpressionTests(TestCase):
    def test_regex_expression(self):
        equation = 'Regex(ATTR, "^dog")'
        value = "doghouse"
        result = evaluate_expression(equation, value)
        self.assertEqual(result, True)

    def test_arithmetic_expression(self):
        equation = "ATTR * 2"
        value = "3"
        result = evaluate_expression(equation, value)
        self.assertEqual(result, 6)

    def test_create_kpi(self):
        """Test creating a single KPI via the API."""
        url = reverse('kpi-create')
        data = {
            "name": "Sample KPI",
            "expression": "ATTR * 2",
            "description": "This is a sample KPI description."
        }
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Sample KPI")
        self.assertEqual(response.json()["expression"], "ATTR * 2")
        self.assertEqual(response.json()["description"], "This is a sample KPI description.")
        self.assertTrue(KPI.objects.filter(name="Sample KPI").exists())

    def test_list_kpis(self):
        """Test listing multiple KPIs."""
        KPI.objects.create(name="KPI 1", expression="ATTR + 1")
        KPI.objects.create(name="KPI 2", expression="ATTR * 2")

        url = reverse('kpi-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["name"], "KPI 1")
        self.assertEqual(response.json()[1]["name"], "KPI 2")

    def test_link_asset_to_kpi(self):
        # Create a KPI to link with an asset
        kpi = KPI.objects.create(name="Link KPI", expression="ATTR - 1")
        url = reverse('kpi-asset-link-create')
        data = {
            "kpi": kpi.id,
            "asset_id": "12345"
        }
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["kpi"], kpi.id)
        self.assertEqual(response.json()["asset_id"], "12345")
        self.assertTrue(KPIAssetLink.objects.filter(kpi=kpi, asset_id="12345").exists())

    def test_evaluate_linked_assets(self):
        # Set up the KPI and link to an asset
        kpi = KPI.objects.create(name="Linked KPI", expression="ATTR + 2")
        KPIAssetLink.objects.create(kpi=kpi, asset_id="123")

        # Sample message to be evaluated
        message = {
            "asset_id": "123",
            "attribute_id": "1",
            "timestamp": "2022-07-31T23:28:37Z[UTC]",
            "value": 5
        }

        # Evaluate and store result based on kpi expression
        evaluate_and_store_result(message, kpi.expression)

        # Parse timestamp for querying
        expected_timestamp = parse_timestamp("2022-07-31T23:28:37Z[UTC]")

        # Verify that the EvaluationResult is stored with correct values
        result = EvaluationResult.objects.filter(
            asset_id="123",
            attribute_id="output_1",
            timestamp=expected_timestamp,
            value="7"
        ).first()

        self.assertIsNotNone(result)
        self.assertEqual(result.value, "7")
