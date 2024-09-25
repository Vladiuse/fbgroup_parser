import logging
from id_parser.src.config import config
from fb.models import FbGroup
from id_parser.src.utils import get_new_urls
from django.db import IntegrityError
import logging

logging.basicConfig(level=logging.INFO)

new_urls = get_new_urls()
errors_count = 0
total_created = 0
for url in new_urls:
    try:
        FbGroup.objects.create(url=url)
        total_created += 1
    except IntegrityError:
        errors_count += 1
logging.info('Created %s, with error %s', total_created, errors_count)









