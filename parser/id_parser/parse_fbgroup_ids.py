import logging

from id_parser.src.usecase import ParseFbGroupsIdsUseCase

logging.basicConfig(level=logging.INFO)
use_case = ParseFbGroupsIdsUseCase()
use_case.parse_groups_ids()