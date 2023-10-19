from configparser import ConfigParser
from pytz import timezone
import os

CONFIG = ConfigParser()
ENV_DEPLOY = os.environ.get('ENV_DEPLOY', 'dev')
CONFIG.read(f'app/setting/conf_{ENV_DEPLOY}.ini')

SERVICE_ACCOUNT_FILE = CONFIG['SERVICE']['ACCOUNT']
JSON_ENTRADA = CONFIG['SERVICE']['JSON_ENTRADA']
PROJECT_MASTER = CONFIG['PROJECT']['PROJECT_MASTER']

# TIMEZONE
TIMEZONE = timezone('America/Lima')

print(f'Environment variables')
print(f'ENV DEPLOY: {ENV_DEPLOY}')
