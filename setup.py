from setuptools import setup, find_packages

setup(
    name='certbot-dns-dnspod-global',
    version='0.1.0',
    description='Certbot plugin for DNSPod Global API',
    author='NGELDragon',
    author_email='m6sin@ngelgames.com',
    url='https://github.com/NGELDragon/certbot-dns-dnspod-global',
    packages=find_packages(),
    install_requires=[
        'requests',
        'certbot',
    ],
    entry_points={
        'certbot.plugins': [
            'dns-dnspod-global = dnspod_global:DnspodGlobalAuthenticator',
        ],
    },
)
