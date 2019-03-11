from collections import OrderedDict
from random import randint

from hmda.resources.hmda_data_options import (
    HMDA_FIELD_DESC_OPTIONS, HMDA_GEO_OPTIONS, HMDA_RECORDS_OPTIONS, HMDA_YEARS
)

# File name format:
# hmda_<year>_<state>_<action>_<format>.zip
# hmda_2016_co_originated-records_labels.zip


def get_data_files(geo, annotations, record_set):
    if geo in HMDA_DATA_FILES:
        return HMDA_DATA_FILES[geo][annotations][record_set]
    else:
        return HMDA_DATA_FILES['nationwide'][annotations][record_set]


# TODO: Remove this and replace it with real files after we calculate file sizes
def generate_fake_files():
    files = OrderedDict()
    for geo, geo_name in HMDA_GEO_OPTIONS:
        files[geo] = OrderedDict()
        for desc, desc_name in HMDA_FIELD_DESC_OPTIONS:
            files[geo][desc] = OrderedDict()
            for record, record_name in HMDA_RECORDS_OPTIONS:
                files[geo][desc][record] = OrderedDict()
                for year, year_name in HMDA_YEARS:
                    zip = 'hmda_{}_{}_{}_{}.zip'.format(year, geo, desc, record)
                    row_count = randint(5000000, 15000000)
                    file_size = '{} GB'.format(randint(3, 19))
                    files[geo][desc][record][year] = \
                        HmdaDataFile(zip, '{:,}'.format(row_count), file_size)
    return files


class HmdaDataFile:
    def __init__(self, file_name, number_of_records, file_size):
        self.file_name = file_name
        self.number_of_records = number_of_records
        self.file_size = file_size


# Access this using HMDA_DATA_FILES[geo][format][action]
HMDA_DATA_FILES = generate_fake_files()

# HMDA_DATA_FILES = {
#     'nationwide': {
#         'labels': {
#             'first-lien-owner-occupied-1-4-family-records': {
#                 '2007': HmdaDataFile('hmda_2007_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '13.9GB'),
#             },
#             'all-records': {
#                 '2007': HmdaDataFile('hmda_2007_nationwide_all-records_labels.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_nationwide_all-records_labels.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_nationwide_all-records_labels.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_nationwide_all-records_labels.zip', 100, '13.9GB'),
#             },
#             'originated-records': {
#                 '2007': HmdaDataFile('hmda_2007_nationwide_originated-records_labels.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_nationwide_originated-records_labels.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_nationwide_originated-records_labels.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_nationwide_originated-records_labels.zip', 100, '13.9GB'),
#             },
#         },
#         'codes': {
#             'first-lien-owner-occupied-1-4-family-records': {
#                 '2007': HmdaDataFile('hmda_2007_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '13.9GB'),
#             },
#             'all-records': {
#                 '2007': HmdaDataFile('hmda_2007_nationwide_all-records_codes.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_nationwide_all-records_codes.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_nationwide_all-records_codes.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_nationwide_all-records_codes.zip', 100, '13.9GB'),
#             },
#             'originated-records': {
#                 '2007': HmdaDataFile('hmda_2007_nationwide_originated-records_codes.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_nationwide_originated-records_codes.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_nationwide_originated-records_codes.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_nationwide_originated-records_codes.zip', 100, '13.9GB'),
#             },
#         },
#     },
#     'al': {
#         'labels': {
#             'first-lien-owner-occupied-1-4-family-records': {
#                 '2007': HmdaDataFile('hmda_2007_al_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_al_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_al_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_al_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '13.9GB'),
#             },
#             'all-records': {
#                 '2007': HmdaDataFile('hmda_2007_al_all-records_labels.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_al_all-records_labels.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_al_all-records_labels.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_al_all-records_labels.zip', 100, '13.9GB'),
#             },
#             'originated-records': {
#                 '2007': HmdaDataFile('hmda_2007_al_originated-records_labels.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_al_originated-records_labels.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_al_originated-records_labels.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_al_originated-records_labels.zip', 100, '13.9GB'),
#             },
#         },
#         'codes': {
#             'first-lien-owner-occupied-1-4-family-records': {
#                 '2007': HmdaDataFile('hmda_2007_al_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_al_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_al_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_al_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '13.9GB'),
#             },
#             'all-records': {
#                 '2007': HmdaDataFile('hmda_2007_al_all-records_codes.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_al_all-records_codes.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_al_all-records_codes.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_al_all-records_codes.zip', 100, '13.9GB'),
#             },
#             'originated-records': {
#                 '2007': HmdaDataFile('hmda_2007_al_originated-records_codes.zip', 100, '13.9GB'),
#                 '2008': HmdaDataFile('hmda_2008_al_originated-records_codes.zip', 100, '13.9GB'),
#                 '2009': HmdaDataFile('hmda_2009_al_originated-records_codes.zip', 100, '13.9GB'),
#                 '2010': HmdaDataFile('hmda_2010_al_originated-records_codes.zip', 100, '13.9GB'),
#             },
#         },
#     }
# }
