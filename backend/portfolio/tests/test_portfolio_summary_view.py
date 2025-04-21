from rest_framework.test import APITestCase

class PortfolioSummaryAPITest(APITestCase):

    def test_missing_params(self):
        response = self.client.get('/api/portfolios/1/summary/')
        self.assertEqual(response.status_code, 400)

    def test_not_found(self):
        response = self.client.get('/api/portfolios/999/summary/?fecha_inicio=2022-02-15&fecha_fin=2022-02-20')
        self.assertEqual(response.status_code, 404)
