import csv
from fb.models import FbGroup as FbGroupModel
from common.config import config

class ResultFileCreator:

    def create(self, groups: list[FbGroupModel]) -> None:
        with open(config.OUTPUT_FILE_PATH, 'x') as file:
            writer = csv.DictWriter(file, delimiter=',', quotechar='"', fieldnames=['group_url', 'ads_count'])
            writer.writeheader()
            for group in groups:
                writer.writerow({
                    'group_url': group.url,
                    'ads_count': group.ads_count,
                })



