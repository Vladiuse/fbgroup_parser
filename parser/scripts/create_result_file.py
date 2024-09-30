import logging
from common.result_file_creator import ResultFileCreator
from fb.models import FbGroup as FbGroupModel
from common.utils import confirm_action


logging.basicConfig(level=logging.INFO)


qs_groups = FbGroupModel.objects.exclude(ads_count__isnull=True).filter(is_used=False).order_by('-ads_count')
logging.info('groups to write: %s', len(qs_groups))
confirm_action()

ResultFileCreator().create(groups=list(qs_groups))
qs_groups.update(is_used=True)