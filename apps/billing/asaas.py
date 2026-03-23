import json
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

_BASE_URLS = {
    'sandbox': 'https://sandbox.asaas.com/api/v3',
    'production': 'https://www.asaas.com/api/v3',
}


class AsaasError(Exception):
    pass


class AsaasClient:
    def __init__(self):
        env = getattr(settings, 'ASAAS_ENVIRONMENT', 'sandbox')
        self.base = _BASE_URLS.get(env, _BASE_URLS['sandbox'])
        self.headers = {
            'access_token': settings.ASAAS_API_KEY,
            'Content-Type': 'application/json',
        }

    def _get(self, path, params=None):
        url = f'{self.base}{path}'
        resp = requests.get(url, headers=self.headers, params=params, timeout=15)
        if not resp.ok:
            logger.error('Asaas GET %s → %s: %s', path, resp.status_code, resp.text)
            raise AsaasError(f'Asaas error {resp.status_code}: {resp.text}')
        return resp.json()

    def _post(self, path, data):
        url = f'{self.base}{path}'
        resp = requests.post(url, headers=self.headers, json=data, timeout=15)
        if not resp.ok:
            logger.error('Asaas POST %s → %s: %s', path, resp.status_code, resp.text)
            raise AsaasError(f'Asaas error {resp.status_code}: {resp.text}')
        return resp.json()

    # ------------------------------------------------------------------
    # Customers
    # ------------------------------------------------------------------

    def create_or_get_customer(self, name: str, email: str, cpf_cnpj: str) -> str:
        """Return Asaas customer ID, creating the customer if needed."""
        # Try to find existing customer by CPF/CNPJ
        result = self._get('/customers', params={'cpfCnpj': cpf_cnpj})
        existing = result.get('data', [])
        if existing:
            return existing[0]['id']

        # Create new customer
        customer = self._post('/customers', {
            'name': name,
            'email': email,
            'cpfCnpj': cpf_cnpj,
        })
        return customer['id']

    # ------------------------------------------------------------------
    # Subscriptions
    # ------------------------------------------------------------------

    _BILLING_TYPES = {
        'pix': 'PIX',
        'credit_card': 'CREDIT_CARD',
    }
    _CYCLES = {
        'monthly': 'MONTHLY',
        'annual': 'YEARLY',
    }

    def create_subscription(
        self,
        customer_id: str,
        billing_type: str,
        billing_cycle: str,
        value: float,
        description: str,
    ) -> dict:
        """
        Create a subscription and return the Asaas response dict.
        The response includes `id` and `invoiceUrl`.
        """
        from datetime import date, timedelta
        next_due = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

        payload = {
            'customer': customer_id,
            'billingType': self._BILLING_TYPES[billing_type],
            'cycle': self._CYCLES[billing_cycle],
            'value': float(value),
            'nextDueDate': next_due,
            'description': description,
        }
        return self._post('/subscriptions', payload)
