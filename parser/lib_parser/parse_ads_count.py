import logging

from lib_parser.src.usecase import ParseGroupsAdsCountUseCase

logging.basicConfig(level=logging.INFO)
ParseGroupsAdsCountUseCase().parse()


