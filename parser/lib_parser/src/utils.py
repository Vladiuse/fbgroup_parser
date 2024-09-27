from fb.models import FbGroup as FbGroupModel


def get_groups_for_parse_ads_count():
    return FbGroupModel.objects.exclude(group_id__isnull=True).filter(ads_count__isnull=True)