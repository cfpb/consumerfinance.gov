# File name format:
# HMDA_<year>_<state>_<action>_<format>.zip
# hmda_2016_co_originated-records_labels.zip


def get_data_files(geo, annotations, record_set):
    if geo in HMDA_DATA_FILES:
        return HMDA_DATA_FILES[geo][annotations][record_set]
    else:
        return HMDA_DATA_FILES['nationwide'][annotations][record_set]


class HmdaDataFile:
    def __init__(self, file_name, number_of_records, file_size):
        self.file_name = file_name
        self.number_of_records = number_of_records
        self.file_size = file_size


# Access this using HMDA_DATA_FILES[geo][format][action]
HMDA_DATA_FILES = {
    'nationwide': {
        'labels': {
            'first-lien-owner-occupied-1-4-family-records': {
                '2007': HmdaDataFile('hmda_2007_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
            },
            'all-records': {
                '2007': HmdaDataFile('hmda_2007_nationwide_all-records_labels.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_nationwide_all-records_labels.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_nationwide_all-records_labels.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_nationwide_all-records_labels.zip', 100, '9.9GB'),
            },
            'originated-records': {
                '2007': HmdaDataFile('hmda_2007_nationwide_originated-records_labels.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_nationwide_originated-records_labels.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_nationwide_originated-records_labels.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_nationwide_originated-records_labels.zip', 100, '9.9GB'),
            },
        },
        'codes': {
            'first-lien-owner-occupied-1-4-family-records': {
                '2007': HmdaDataFile('hmda_2007_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
            },
            'all-records': {
                '2007': HmdaDataFile('hmda_2007_nationwide_all-records_codes.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_nationwide_all-records_codes.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_nationwide_all-records_codes.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_nationwide_all-records_codes.zip', 100, '9.9GB'),
            },
            'originated-records': {
                '2007': HmdaDataFile('hmda_2007_nationwide_originated-records_codes.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_nationwide_originated-records_codes.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_nationwide_originated-records_codes.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_nationwide_originated-records_codes.zip', 100, '9.9GB'),
            },
        },
    },
    'al': {
        'labels': {
            'first-lien-owner-occupied-1-4-family-records': {
                '2007': HmdaDataFile('hmda_2007_al_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_al_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_al_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_al_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
            },
            'all-records': {
                '2007': HmdaDataFile('hmda_2007_al_all-records_labels.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_al_all-records_labels.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_al_all-records_labels.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_al_all-records_labels.zip', 100, '9.9GB'),
            },
            'originated-records': {
                '2007': HmdaDataFile('hmda_2007_al_originated-records_labels.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_al_originated-records_labels.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_al_originated-records_labels.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_al_originated-records_labels.zip', 100, '9.9GB'),
            },
        },
        'codes': {
            'first-lien-owner-occupied-1-4-family-records': {
                '2007': HmdaDataFile('hmda_2007_al_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_al_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_al_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_al_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
            },
            'all-records': {
                '2007': HmdaDataFile('hmda_2007_al_all-records_codes.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_al_all-records_codes.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_al_all-records_codes.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_al_all-records_codes.zip', 100, '9.9GB'),
            },
            'originated-records': {
                '2007': HmdaDataFile('hmda_2007_al_originated-records_codes.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_al_originated-records_codes.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_al_originated-records_codes.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_al_originated-records_codes.zip', 100, '9.9GB'),
            },
        },
    },
    'ak': {
        'labels': {
            'first-lien-owner-occupied-1-4-family-records': {
                '2007': HmdaDataFile('hmda_2007_ak_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_ak_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_ak_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_ak_first-lien-owner-occupied-1-4-family-records_labels.zip', 100, '9.9GB'),
            },
            'all-records': {
                '2007': HmdaDataFile('hmda_2007_ak_all-records_labels.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_ak_all-records_labels.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_ak_all-records_labels.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_ak_all-records_labels.zip', 100, '9.9GB'),
            },
            'originated-records': {
                '2007': HmdaDataFile('hmda_2007_ak_originated-records_labels.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_ak_originated-records_labels.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_ak_originated-records_labels.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_ak_originated-records_labels.zip', 100, '9.9GB'),
            },
        },
        'codes': {
            'first-lien-owner-occupied-1-4-family-records': {
                '2007': HmdaDataFile('hmda_2007_ak_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_ak_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_ak_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_ak_first-lien-owner-occupied-1-4-family-records_codes.zip', 100, '9.9GB'),
            },
            'all-records': {
                '2007': HmdaDataFile('hmda_2007_ak_all-records_codes.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_ak_all-records_codes.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_ak_all-records_codes.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_ak_all-records_codes.zip', 100, '9.9GB'),
            },
            'originated-records': {
                '2007': HmdaDataFile('hmda_2007_ak_originated-records_codes.zip', 100, '9.9GB'),
                '2008': HmdaDataFile('hmda_2008_ak_originated-records_codes.zip', 100, '9.9GB'),
                '2009': HmdaDataFile('hmda_2009_ak_originated-records_codes.zip', 100, '9.9GB'),
                '2010': HmdaDataFile('hmda_2010_ak_originated-records_codes.zip', 100, '9.9GB'),
            },
        },
    },
    # ... remaining states go here
}
