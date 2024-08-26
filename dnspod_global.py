import requests
import logging

logger = logging.getLogger(__name__)

DNSPOD_API_URL = 'https://api.dnspod.com/'

class DnspodGlobalClient:
    def __init__(self, api_id, api_token):
        self.api_id = api_id
        self.api_token = api_token

    def _make_request(self, action, data):
        url = DNSPOD_API_URL + action
        data.update({
            'login_token': f'{self.api_id},{self.api_token}',
            'format': 'json'
        })
        response = requests.post(url, data=data)
        response.raise_for_status()
        result = response.json()
        if result.get('status', {}).get('code') != '1':
            raise Exception(f"API request failed: {result.get('status', {}).get('message')}")
        return result

    def add_txt_record(self, domain, sub_domain, value):
        action = 'Record.Create'
        data = {
            'domain': domain,
            'sub_domain': sub_domain,
            'record_type': 'TXT',
            'record_line': '默认',
            'value': value,
        }
        return self._make_request(action, data)

    def del_txt_record(self, domain, record_id):
        action = 'Record.Remove'
        data = {
            'domain': domain,
            'record_id': record_id,
        }
        return self._make_request(action, data)
