import logging
from common.result_file_creator import FollowersLikesCountResultFile
from fb.models import FbGroup as FbGroupModel
from common.utils import confirm_action


logging.basicConfig(level=logging.INFO)


# qs_ads_count_groups = FbGroupModel.objects.exclude(ads_count__isnull=True).filter(is_used=False).order_by('-ads_count')
qs_followers_count = FbGroupModel.objects.filter(followers_count__isnull=False).filter(is_used=False).order_by('-followers_count')
qs = qs_followers_count
logging.info('groups to write: %s', len(qs))
confirm_action()
groups_len = int(input('Set len of groups: '))
qs = qs[:groups_len]
FollowersLikesCountResultFile().create(groups=list(qs))
print(qs.update(is_used=True))