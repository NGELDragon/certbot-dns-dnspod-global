import requests
import logging

from certbot.plugins.dns_common import DNSAuthenticator, CredentialsConfiguration
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
            'record_line': 'default',
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


class DnspodGlobalAuthenticator(DNSAuthenticator):
    description = 'Obtain certificates using a DNS TXT record (if you are using DNSPod for DNS).'

    def __init__(self, *args, **kwargs):
        super(DnspodGlobalAuthenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(DnspodGlobalAuthenticator, cls).add_parser_arguments(add)
        add('credentials', help='Path to the DNSPod credentials INI file.')

    def more_info(self):
        return 'This plugin configures a DNS TXT record to prove domain ownership using the DNSPod API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'DNSPod credentials INI file',
            {
                'api-id': 'API ID for DNSPod account, obtained from https://account.dnspod.com/account/token',
                'api-token': 'API Token for DNSPod account, obtained from https://account.dnspod.com/account/token',
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_dnspod_client().add_txt_record(
            self._get_domain(domain),
            self._get_subdomain(validation_name),
            validation
        )

    def _cleanup(self, domain, validation_name, validation):
        record_id = self._find_record_id(domain, validation_name, validation)
        self._get_dnspod_client().del_txt_record(self._get_domain(domain), record_id)

    def _get_dnspod_client(self):
        return DnspodGlobalClient(
            self.credentials.conf('api-id'),
            self.credentials.conf('api-token')
        )

    def _get_domain(self, domain):
        return domain.split('.')[-2] + '.' + domain.split('.')[-1]

    def _get_subdomain(self, validation_name):
        return validation_name.split('.')[0]

    def _find_record_id(self, domain, subdomain, value):
        # 해당 서브도메인과 값을 가진 TXT 레코드의 ID를 찾음
        records = self._get_dnspod_client().list_records(domain, subdomain, 'TXT')
        for record in records.get('records', []):
            if record['value'] == value:
                return record['id']
        return None
