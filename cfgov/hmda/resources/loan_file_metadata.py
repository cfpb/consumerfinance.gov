# flake8: noqa: B950
from hmda.models.hmda_data_file import HmdaDataFile


# Access this using HMDA_DATA_FILES[geo][field_descriptions][records]
LOAN_FILE_METADATA = {
    "nationwide": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "7036352",
                    "482.83 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "7201366",
                    "453.04 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "5986659",
                    "369.82 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "6113423",
                    "485.63 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "4832425",
                    "323.43 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "5526941",
                    "330.65 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "7783986",
                    "467.08 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "5946435",
                    "399.41 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "6764902",
                    "455.07 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "7126202",
                    "492.02 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "8298882",
                    "573.78 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nationwide_all-records_labels.zip",
                    "16332987",
                    "1.2 GB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nationwide_all-records_labels.zip",
                    "26605695",
                    "1.72 GB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nationwide_all-records_labels.zip",
                    "14285496",
                    "986 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nationwide_all-records_labels.zip",
                    "14374184",
                    "1.21 GB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nationwide_all-records_labels.zip",
                    "12049341",
                    "862.92 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nationwide_all-records_labels.zip",
                    "17391570",
                    "1.06 GB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nationwide_all-records_labels.zip",
                    "19493491",
                    "1.29 GB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nationwide_all-records_labels.zip",
                    "14873415",
                    "1.08 GB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nationwide_all-records_labels.zip",
                    "16348557",
                    "1.19 GB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nationwide_all-records_labels.zip",
                    "17016159",
                    "1.27 GB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nationwide_all-records_labels.zip",
                    "18691551",
                    "1.4 GB",
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nationwide_originated-records_labels.zip",
                    "8377907",
                    "457.12 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nationwide_originated-records_labels.zip",
                    "10441545",
                    "528.7 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nationwide_originated-records_labels.zip",
                    "7339057",
                    "247.2 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nationwide_originated-records_labels.zip",
                    "7404258",
                    "461.08 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nationwide_originated-records_labels.zip",
                    "6039826",
                    "331.36 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nationwide_originated-records_labels.zip",
                    "7177262",
                    "360.36 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nationwide_originated-records_labels.zip",
                    "8950936",
                    "416.67 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nationwide_originated-records_labels.zip",
                    "7095262",
                    "381.6 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nationwide_originated-records_labels.zip",
                    "7863337",
                    "419.27 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nationwide_originated-records_labels.zip",
                    "8706657",
                    "476.47 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nationwide_originated-records_labels.zip",
                    "9783966",
                    "529.5 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "7036352",
                    "165.84 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "7201366",
                    "141.73 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "5986659",
                    "77.47 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "6113423",
                    "144.37 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "4832425",
                    "213.95 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "5526941",
                    "107.3 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "7783986",
                    "140.57 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "5946435",
                    "132 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "6764902",
                    "149.36 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "7126202",
                    "166.47 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nationwide_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "8298882",
                    "189.65 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nationwide_all-records_codes.zip",
                    "16332987",
                    "384.11 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nationwide_all-records_codes.zip",
                    "26605695",
                    "461.15 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nationwide_all-records_codes.zip",
                    "14285496",
                    "182.02 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nationwide_all-records_codes.zip",
                    "14374184",
                    "337.27 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nationwide_all-records_codes.zip",
                    "12049341",
                    "537.81 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nationwide_all-records_codes.zip",
                    "17391570",
                    "309.22 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nationwide_all-records_codes.zip",
                    "19493491",
                    "331.31 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nationwide_all-records_codes.zip",
                    "14873415",
                    "335.22 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nationwide_all-records_codes.zip",
                    "16348557",
                    "367.78 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nationwide_all-records_codes.zip",
                    "17016159",
                    "400.19 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nationwide_all-records_codes.zip",
                    "18691551",
                    "434.69 MB",
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nationwide_originated-records_codes.zip",
                    "8377907",
                    "196.62 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nationwide_originated-records_codes.zip",
                    "10441545",
                    "199.55 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nationwide_originated-records_codes.zip",
                    "7339057",
                    "94.95 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nationwide_originated-records_codes.zip",
                    "7404258",
                    "173.96 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nationwide_originated-records_codes.zip",
                    "6039826",
                    "233.64 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nationwide_originated-records_codes.zip",
                    "7177262",
                    "137.98 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nationwide_originated-records_codes.zip",
                    "8950936",
                    "162.04 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nationwide_originated-records_codes.zip",
                    "7095262",
                    "157.4 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nationwide_originated-records_codes.zip",
                    "7863337",
                    "173.45 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nationwide_originated-records_codes.zip",
                    "8706657",
                    "203.33 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nationwide_originated-records_codes.zip",
                    "9783966",
                    "224.11 MB",
                ),
            },
        },
    },
    "va": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_va_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "216152",
                    "11.27 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_va_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "228323",
                    "11.15 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_va_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "175737",
                    "5.58 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_va_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "191048",
                    "11.13 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_va_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "147744",
                    "7.63 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_va_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "186185",
                    "8.91 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_va_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "273787",
                    "12.14 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_va_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "205670",
                    "10.53 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_va_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "228664",
                    "11.48 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_va_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "244599",
                    "12.77 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_va_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "288436",
                    "14.9 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_va_all-records_labels.zip", "494057", "27.35 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_va_all-records_labels.zip", "784919", "38.17 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_va_all-records_labels.zip", "411507", "14.48 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_va_all-records_labels.zip", "445447", "27.97 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_va_all-records_labels.zip", "365572", "20.34 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_va_all-records_labels.zip", "539572", "26.49 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_va_all-records_labels.zip", "637212", "29.34 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_va_all-records_labels.zip", "482943", "27.06 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_va_all-records_labels.zip", "517819", "28.54 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_va_all-records_labels.zip", "563167", "31.8 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_va_all-records_labels.zip", "634102", "35.59 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_va_originated-records_labels.zip",
                    "252237",
                    "13.42 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_va_originated-records_labels.zip",
                    "327766",
                    "16.15 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_va_originated-records_labels.zip",
                    "211218",
                    "6.89 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_va_originated-records_labels.zip",
                    "227837",
                    "13.49 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_va_originated-records_labels.zip",
                    "183729",
                    "9.73 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_va_originated-records_labels.zip",
                    "234813",
                    "11.47 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_va_originated-records_labels.zip",
                    "308658",
                    "13.99 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_va_originated-records_labels.zip",
                    "239310",
                    "12.46 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_va_originated-records_labels.zip",
                    "260214",
                    "13.38 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_va_originated-records_labels.zip",
                    "294145",
                    "15.54 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_va_originated-records_labels.zip",
                    "334770",
                    "17.51 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_va_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "216152",
                    "7.74 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_va_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "228323",
                    "7.71 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_va_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "175737",
                    "3.89 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_va_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "191048",
                    "7.65 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_va_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "147744",
                    "5.26 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_va_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "186185",
                    "6.21 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_va_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "273787",
                    "8.61 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_va_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "205670",
                    "7.08 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_va_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "228664",
                    "7.72 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_va_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "244599",
                    "8.81 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_va_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "288436",
                    "10.21 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_va_all-records_codes.zip", "494057", "18.2 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_va_all-records_codes.zip", "784919", "25.76 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_va_all-records_codes.zip", "411507", "9.31 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_va_all-records_codes.zip", "445447", "18.51 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_va_all-records_codes.zip", "365572", "13.57 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_va_all-records_codes.zip", "539572", "17.99 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_va_all-records_codes.zip", "637212", "20.26 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_va_all-records_codes.zip", "482943", "17.83 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_va_all-records_codes.zip", "517819", "18.81 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_va_all-records_codes.zip", "563167", "21.36 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_va_all-records_codes.zip", "634102", "23.86 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_va_originated-records_codes.zip",
                    "252237",
                    "9.19 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_va_originated-records_codes.zip",
                    "327766",
                    "11.21 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_va_originated-records_codes.zip",
                    "211218",
                    "4.75 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_va_originated-records_codes.zip",
                    "227837",
                    "9.22 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_va_originated-records_codes.zip",
                    "183729",
                    "6.67 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_va_originated-records_codes.zip",
                    "234813",
                    "7.98 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_va_originated-records_codes.zip",
                    "308658",
                    "9.9 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_va_originated-records_codes.zip",
                    "239310",
                    "8.34 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_va_originated-records_codes.zip",
                    "260214",
                    "8.98 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_va_originated-records_codes.zip",
                    "294145",
                    "10.63 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_va_originated-records_codes.zip",
                    "334770",
                    "11.93 MB",
                ),
            },
        },
    },
    "co": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_co_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "228866",
                    "11.12 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_co_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "144805",
                    "6.71 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_co_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "182654",
                    "5.82 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_co_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "194123",
                    "10.51 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_co_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "139220",
                    "6.92 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_co_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "128542",
                    "5.81 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_co_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "209511",
                    "8.79 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_co_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "149880",
                    "7.07 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_co_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "180911",
                    "8.7 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_co_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "192627",
                    "9.59 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_co_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "222498",
                    "10.92 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_co_all-records_labels.zip", "483436", "25.25 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_co_all-records_labels.zip", "537363", "25.41 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_co_all-records_labels.zip", "404517", "14.76 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_co_all-records_labels.zip", "409511", "23.35 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_co_all-records_labels.zip", "313445", "16.62 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_co_all-records_labels.zip", "370468", "17.59 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_co_all-records_labels.zip", "492317", "21.47 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_co_all-records_labels.zip", "366969", "18.87 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_co_all-records_labels.zip", "413027", "21.58 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_co_all-records_labels.zip", "427952", "22.81 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_co_all-records_labels.zip", "474846", "24.96 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_co_originated-records_labels.zip",
                    "263402",
                    "13.07 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_co_originated-records_labels.zip",
                    "218842",
                    "10.18 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_co_originated-records_labels.zip",
                    "216848",
                    "7.17 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_co_originated-records_labels.zip",
                    "227578",
                    "12.54 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_co_originated-records_labels.zip",
                    "169959",
                    "8.6 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_co_originated-records_labels.zip",
                    "162244",
                    "7.43 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_co_originated-records_labels.zip",
                    "236219",
                    "9.99 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_co_originated-records_labels.zip",
                    "179323",
                    "8.69 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_co_originated-records_labels.zip",
                    "207951",
                    "10.35 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_co_originated-records_labels.zip",
                    "235157",
                    "11.95 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_co_originated-records_labels.zip",
                    "263229",
                    "13.2 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_co_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "228866",
                    "7.81 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_co_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "144805",
                    "4.75 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_co_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "182654",
                    "4.07 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_co_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "194123",
                    "7.52 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_co_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "139220",
                    "4.9 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_co_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "128542",
                    "4.11 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_co_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "209511",
                    "6.34 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_co_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "149880",
                    "4.88 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_co_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "180911",
                    "6.03 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_co_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "192627",
                    "6.74 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_co_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "222498",
                    "7.6 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_co_all-records_codes.zip", "483436", "17.2 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_co_all-records_codes.zip", "537363", "17.72 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_co_all-records_codes.zip", "404517", "9.9 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_co_all-records_codes.zip", "409511", "16.01 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_co_all-records_codes.zip", "313445", "11.43 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_co_all-records_codes.zip", "370468", "12.3 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_co_all-records_codes.zip", "492317", "15.15 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_co_all-records_codes.zip", "366969", "12.63 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_co_all-records_codes.zip", "413027", "14.47 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_co_all-records_codes.zip", "427952", "15.58 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_co_all-records_codes.zip", "474846", "16.87 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_co_originated-records_codes.zip",
                    "263402",
                    "9.15 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_co_originated-records_codes.zip",
                    "218842",
                    "7.18 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_co_originated-records_codes.zip",
                    "216848",
                    "4.99 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_co_originated-records_codes.zip",
                    "227578",
                    "8.91 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_co_originated-records_codes.zip",
                    "169959",
                    "6.05 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_co_originated-records_codes.zip",
                    "162244",
                    "5.23 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_co_originated-records_codes.zip",
                    "236219",
                    "7.16 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_co_originated-records_codes.zip",
                    "179323",
                    "5.95 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_co_originated-records_codes.zip",
                    "207951",
                    "7.15 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_co_originated-records_codes.zip",
                    "235157",
                    "8.37 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_co_originated-records_codes.zip",
                    "263229",
                    "9.16 MB",
                ),
            },
        },
    },
    "vi": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "0",
                    "647 bytes",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "0",
                    "647 bytes",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15",
                    "1.55 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "0",
                    "647 bytes",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "0",
                    "647 bytes",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "0",
                    "647 bytes",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "0",
                    "647 bytes",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "0",
                    "647 bytes",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "0",
                    "647 bytes",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "0",
                    "647 bytes",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "0",
                    "647 bytes",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vi_all-records_labels.zip", "0", "581 bytes"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vi_all-records_labels.zip", "0", "581 bytes"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vi_all-records_labels.zip", "47", "2.39 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vi_all-records_labels.zip", "0", "581 bytes"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vi_all-records_labels.zip", "0", "581 bytes"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vi_all-records_labels.zip", "0", "581 bytes"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vi_all-records_labels.zip", "0", "581 bytes"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vi_all-records_labels.zip", "0", "581 bytes"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vi_all-records_labels.zip", "0", "581 bytes"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vi_all-records_labels.zip", "0", "581 bytes"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vi_all-records_labels.zip", "0", "581 bytes"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vi_originated-records_labels.zip",
                    "0",
                    "595 bytes",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vi_originated-records_labels.zip",
                    "0",
                    "595 bytes",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vi_originated-records_labels.zip",
                    "23",
                    "1.73 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vi_originated-records_labels.zip",
                    "0",
                    "595 bytes",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vi_originated-records_labels.zip",
                    "0",
                    "595 bytes",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vi_originated-records_labels.zip",
                    "0",
                    "595 bytes",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vi_originated-records_labels.zip",
                    "0",
                    "595 bytes",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vi_originated-records_labels.zip",
                    "0",
                    "595 bytes",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vi_originated-records_labels.zip",
                    "0",
                    "595 bytes",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vi_originated-records_labels.zip",
                    "0",
                    "595 bytes",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vi_originated-records_labels.zip",
                    "0",
                    "595 bytes",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "0",
                    "540 bytes",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "0",
                    "540 bytes",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15",
                    "940 bytes",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "0",
                    "540 bytes",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "0",
                    "540 bytes",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "0",
                    "540 bytes",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "0",
                    "540 bytes",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "0",
                    "540 bytes",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "0",
                    "540 bytes",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "0",
                    "540 bytes",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "0",
                    "540 bytes",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vi_all-records_codes.zip", "0", "474 bytes"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vi_all-records_codes.zip", "0", "474 bytes"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vi_all-records_codes.zip", "47", "1.37 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vi_all-records_codes.zip", "0", "474 bytes"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vi_all-records_codes.zip", "0", "474 bytes"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vi_all-records_codes.zip", "0", "474 bytes"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vi_all-records_codes.zip", "0", "474 bytes"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vi_all-records_codes.zip", "0", "474 bytes"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vi_all-records_codes.zip", "0", "474 bytes"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vi_all-records_codes.zip", "0", "474 bytes"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vi_all-records_codes.zip", "0", "474 bytes"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vi_originated-records_codes.zip",
                    "0",
                    "488 bytes",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vi_originated-records_codes.zip",
                    "0",
                    "488 bytes",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vi_originated-records_codes.zip",
                    "23",
                    "1.03 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vi_originated-records_codes.zip",
                    "0",
                    "488 bytes",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vi_originated-records_codes.zip",
                    "0",
                    "488 bytes",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vi_originated-records_codes.zip",
                    "0",
                    "488 bytes",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vi_originated-records_codes.zip",
                    "0",
                    "488 bytes",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vi_originated-records_codes.zip",
                    "0",
                    "488 bytes",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vi_originated-records_codes.zip",
                    "0",
                    "488 bytes",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vi_originated-records_codes.zip",
                    "0",
                    "488 bytes",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vi_originated-records_codes.zip",
                    "0",
                    "488 bytes",
                ),
            },
        },
    },
    "ak": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ak_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15356",
                    "685.22 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ak_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "16758",
                    "627.93 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ak_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12579",
                    "350.04 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ak_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "14511",
                    "637.91 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ak_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12147",
                    "530.18 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ak_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15576",
                    "536.13 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ak_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "23301",
                    "812.74 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ak_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "16974",
                    "682.85 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ak_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "18636",
                    "750.13 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ak_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "17337",
                    "684.52 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ak_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "22064",
                    "872.42 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ak_all-records_labels.zip", "36105", "1.77 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ak_all-records_labels.zip", "48143", "2.05 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ak_all-records_labels.zip", "28632", "904.87 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ak_all-records_labels.zip", "33421", "1.59 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ak_all-records_labels.zip", "26499", "1.29 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ak_all-records_labels.zip", "36410", "1.47 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ak_all-records_labels.zip", "51821", "2.02 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ak_all-records_labels.zip", "36900", "1.62 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ak_all-records_labels.zip", "41203", "1.81 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ak_all-records_labels.zip", "39394", "1.81 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ak_all-records_labels.zip", "46691", "2.09 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ak_originated-records_labels.zip",
                    "17503",
                    "792.19 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ak_originated-records_labels.zip",
                    "21167",
                    "801.83 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ak_originated-records_labels.zip",
                    "14430",
                    "400.6 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ak_originated-records_labels.zip",
                    "16680",
                    "749.38 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ak_originated-records_labels.zip",
                    "14272",
                    "633.57 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ak_originated-records_labels.zip",
                    "17485",
                    "614.3 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ak_originated-records_labels.zip",
                    "24987",
                    "878.94 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ak_originated-records_labels.zip",
                    "19236",
                    "785.43 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ak_originated-records_labels.zip",
                    "20697",
                    "847.87 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ak_originated-records_labels.zip",
                    "20363",
                    "840.47 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ak_originated-records_labels.zip",
                    "24887",
                    "1.02 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ak_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15356",
                    "426.06 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ak_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "16758",
                    "411.75 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ak_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12579",
                    "240.69 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ak_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "14511",
                    "394.05 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ak_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12147",
                    "329.2 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ak_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15576",
                    "364.56 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ak_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "23301",
                    "544.64 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ak_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "16974",
                    "426.2 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ak_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "18636",
                    "464.07 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ak_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "17337",
                    "417.9 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ak_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "22064",
                    "530.98 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ak_all-records_codes.zip", "36105", "1.07 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ak_all-records_codes.zip", "48143", "1.24 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ak_all-records_codes.zip", "28632", "571.83 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ak_all-records_codes.zip", "33421", "951.9 KB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ak_all-records_codes.zip", "26499", "778.42 KB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ak_all-records_codes.zip", "36410", "899.28 KB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ak_all-records_codes.zip", "51821", "1.29 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ak_all-records_codes.zip", "36900", "992.55 KB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ak_all-records_codes.zip", "41203", "1.1 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ak_all-records_codes.zip", "39394", "1.01 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ak_all-records_codes.zip", "46691", "1.17 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ak_originated-records_codes.zip",
                    "17503",
                    "490.92 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ak_originated-records_codes.zip",
                    "21167",
                    "527.65 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ak_originated-records_codes.zip",
                    "14430",
                    "275.46 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ak_originated-records_codes.zip",
                    "16680",
                    "458.98 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ak_originated-records_codes.zip",
                    "14272",
                    "392.19 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ak_originated-records_codes.zip",
                    "17485",
                    "413.46 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ak_originated-records_codes.zip",
                    "24987",
                    "583.23 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ak_originated-records_codes.zip",
                    "19236",
                    "488.12 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ak_originated-records_codes.zip",
                    "20697",
                    "518.32 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ak_originated-records_codes.zip",
                    "20363",
                    "514.87 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ak_originated-records_codes.zip",
                    "24887",
                    "617.44 KB",
                ),
            },
        },
    },
    "al": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_al_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "86522",
                    "4.16 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_al_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "106195",
                    "4.88 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_al_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "80115",
                    "2.33 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_al_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "75252",
                    "4.13 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_al_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "63808",
                    "3.06 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_al_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "89932",
                    "4.1 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_al_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "103427",
                    "4.47 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_al_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "75467",
                    "3.54 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_al_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "87005",
                    "3.98 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_al_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "93236",
                    "4.39 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_al_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "99531",
                    "4.7 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_al_all-records_labels.zip", "226918", "11.95 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_al_all-records_labels.zip", "367991", "17.47 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_al_all-records_labels.zip", "209002", "7.08 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_al_all-records_labels.zip", "205039", "11.99 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_al_all-records_labels.zip", "182825", "9.57 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_al_all-records_labels.zip", "286567", "13.72 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_al_all-records_labels.zip", "294820", "13.87 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_al_all-records_labels.zip", "228420", "11.89 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_al_all-records_labels.zip", "249347", "12.77 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_al_all-records_labels.zip", "253915", "13.16 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_al_all-records_labels.zip", "264313", "13.66 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_al_originated-records_labels.zip",
                    "109870",
                    "5.39 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_al_originated-records_labels.zip",
                    "153334",
                    "7.1 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_al_originated-records_labels.zip",
                    "103096",
                    "3.05 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_al_originated-records_labels.zip",
                    "98097",
                    "5.48 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_al_originated-records_labels.zip",
                    "85899",
                    "4.21 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_al_originated-records_labels.zip",
                    "119306",
                    "5.51 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_al_originated-records_labels.zip",
                    "126063",
                    "5.57 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_al_originated-records_labels.zip",
                    "97761",
                    "4.65 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_al_originated-records_labels.zip",
                    "106706",
                    "4.95 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_al_originated-records_labels.zip",
                    "118638",
                    "5.68 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_al_originated-records_labels.zip",
                    "123170",
                    "5.93 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_al_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "86522",
                    "2.77 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_al_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "106195",
                    "3.34 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_al_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "80115",
                    "1.67 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_al_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "75252",
                    "2.81 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_al_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "63808",
                    "2.06 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_al_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "89932",
                    "2.83 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_al_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "103427",
                    "3.06 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_al_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "75467",
                    "2.35 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_al_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "87005",
                    "2.64 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_al_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "93236",
                    "2.92 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_al_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "99531",
                    "3.15 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_al_all-records_codes.zip", "226918", "7.69 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_al_all-records_codes.zip", "367991", "11.49 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_al_all-records_codes.zip", "209002", "4.77 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_al_all-records_codes.zip", "205039", "7.82 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_al_all-records_codes.zip", "182825", "6.25 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_al_all-records_codes.zip", "286567", "9.04 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_al_all-records_codes.zip", "294820", "9.23 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_al_all-records_codes.zip", "228420", "7.78 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_al_all-records_codes.zip", "249347", "8.38 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_al_all-records_codes.zip", "253915", "8.52 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_al_all-records_codes.zip", "264313", "9.06 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_al_originated-records_codes.zip",
                    "109870",
                    "3.56 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_al_originated-records_codes.zip",
                    "153334",
                    "4.85 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_al_originated-records_codes.zip",
                    "103096",
                    "2.14 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_al_originated-records_codes.zip",
                    "98097",
                    "3.71 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_al_originated-records_codes.zip",
                    "85899",
                    "2.8 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_al_originated-records_codes.zip",
                    "119306",
                    "3.78 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_al_originated-records_codes.zip",
                    "126063",
                    "3.8 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_al_originated-records_codes.zip",
                    "97761",
                    "3.07 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_al_originated-records_codes.zip",
                    "106706",
                    "3.27 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_al_originated-records_codes.zip",
                    "118638",
                    "3.76 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_al_originated-records_codes.zip",
                    "123170",
                    "3.94 MB",
                ),
            },
        },
    },
    "ar": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ar_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "49025",
                    "2.38 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ar_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "55026",
                    "2.46 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ar_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "45327",
                    "1.49 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ar_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "42845",
                    "2.26 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ar_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "37601",
                    "1.77 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ar_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "49034",
                    "2.14 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ar_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "61531",
                    "2.65 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ar_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "46801",
                    "2.1 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ar_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "54493",
                    "2.37 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ar_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "54893",
                    "2.56 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ar_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "61834",
                    "2.8 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ar_all-records_labels.zip", "131352", "6.97 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ar_all-records_labels.zip", "179146", "8.6 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ar_all-records_labels.zip", "125392", "4.6 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ar_all-records_labels.zip", "118384", "6.72 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ar_all-records_labels.zip", "108526", "5.63 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ar_all-records_labels.zip", "141191", "6.71 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ar_all-records_labels.zip", "159208", "7.41 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ar_all-records_labels.zip", "127757", "6.44 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ar_all-records_labels.zip", "142441", "7.13 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ar_all-records_labels.zip", "146285", "7.61 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ar_all-records_labels.zip", "154830", "7.85 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ar_originated-records_labels.zip",
                    "65762",
                    "3.27 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ar_originated-records_labels.zip",
                    "83327",
                    "3.71 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ar_originated-records_labels.zip",
                    "62259",
                    "2.05 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ar_originated-records_labels.zip",
                    "59384",
                    "3.2 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ar_originated-records_labels.zip",
                    "52994",
                    "2.56 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ar_originated-records_labels.zip",
                    "71395",
                    "3.11 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ar_originated-records_labels.zip",
                    "78016",
                    "3.4 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ar_originated-records_labels.zip",
                    "62549",
                    "2.86 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ar_originated-records_labels.zip",
                    "69315",
                    "3.08 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ar_originated-records_labels.zip",
                    "73125",
                    "3.48 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ar_originated-records_labels.zip",
                    "79283",
                    "3.68 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ar_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "49025",
                    "1.56 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ar_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "55026",
                    "1.62 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ar_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "45327",
                    "1.04 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ar_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "42845",
                    "1.51 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ar_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "37601",
                    "1.16 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ar_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "49034",
                    "1.41 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ar_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "61531",
                    "1.81 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ar_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "46801",
                    "1.35 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ar_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "54493",
                    "1.53 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ar_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "54893",
                    "1.65 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ar_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "61834",
                    "1.81 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ar_all-records_codes.zip", "131352", "4.44 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ar_all-records_codes.zip", "179146", "5.43 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ar_all-records_codes.zip", "125392", "3.01 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ar_all-records_codes.zip", "118384", "4.33 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ar_all-records_codes.zip", "108526", "3.58 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ar_all-records_codes.zip", "141191", "4.14 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ar_all-records_codes.zip", "159208", "4.87 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ar_all-records_codes.zip", "127757", "4.13 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ar_all-records_codes.zip", "142441", "4.51 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ar_all-records_codes.zip", "146285", "4.87 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ar_all-records_codes.zip", "154830", "5.04 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ar_originated-records_codes.zip",
                    "65762",
                    "2.1 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ar_originated-records_codes.zip",
                    "83327",
                    "2.43 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ar_originated-records_codes.zip",
                    "62259",
                    "1.41 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ar_originated-records_codes.zip",
                    "59384",
                    "2.11 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ar_originated-records_codes.zip",
                    "52994",
                    "1.65 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ar_originated-records_codes.zip",
                    "71395",
                    "2.03 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ar_originated-records_codes.zip",
                    "78016",
                    "2.3 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ar_originated-records_codes.zip",
                    "62549",
                    "1.82 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ar_originated-records_codes.zip",
                    "69315",
                    "1.96 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ar_originated-records_codes.zip",
                    "73125",
                    "2.21 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ar_originated-records_codes.zip",
                    "79283",
                    "2.34 MB",
                ),
            },
        },
    },
    "vt": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "11252",
                    "465.67 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "13430",
                    "571.04 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "9250",
                    "291.43 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "10215",
                    "455.27 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "8361",
                    "346.05 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12079",
                    "491.28 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "21026",
                    "782.79 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "13512",
                    "578.18 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15651",
                    "620.42 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "14400",
                    "594.85 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "17914",
                    "703.52 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vt_all-records_labels.zip", "25971", "1.19 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vt_all-records_labels.zip", "43664", "1.95 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vt_all-records_labels.zip", "22335", "765.5 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vt_all-records_labels.zip", "24028", "1.19 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vt_all-records_labels.zip", "20816", "953.84 KB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vt_all-records_labels.zip", "33040", "1.44 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vt_all-records_labels.zip", "46532", "1.87 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vt_all-records_labels.zip", "32687", "1.56 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vt_all-records_labels.zip", "36637", "1.61 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vt_all-records_labels.zip", "32790", "1.49 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vt_all-records_labels.zip", "37869", "1.66 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vt_originated-records_labels.zip",
                    "15176",
                    "645.84 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vt_originated-records_labels.zip",
                    "20755",
                    "882.15 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vt_originated-records_labels.zip",
                    "13325",
                    "425.68 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vt_originated-records_labels.zip",
                    "14053",
                    "645.96 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vt_originated-records_labels.zip",
                    "11893",
                    "504.52 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vt_originated-records_labels.zip",
                    "17432",
                    "722.72 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vt_originated-records_labels.zip",
                    "25699",
                    "980.48 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vt_originated-records_labels.zip",
                    "17791",
                    "786.1 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vt_originated-records_labels.zip",
                    "19808",
                    "804.9 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vt_originated-records_labels.zip",
                    "19293",
                    "814.7 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vt_originated-records_labels.zip",
                    "22745",
                    "914.05 KB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "11252",
                    "290.62 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "13430",
                    "365.86 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "9250",
                    "198.27 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "10215",
                    "285.97 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "8361",
                    "216.87 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12079",
                    "314.55 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "21026",
                    "510.88 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "13512",
                    "361.01 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15651",
                    "386.89 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "14400",
                    "367.68 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "17914",
                    "433.81 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vt_all-records_codes.zip", "25971", "716.41 KB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vt_all-records_codes.zip", "43664", "1.22 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vt_all-records_codes.zip", "22335", "486.85 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vt_all-records_codes.zip", "24028", "719.81 KB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vt_all-records_codes.zip", "20816", "576.12 KB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vt_all-records_codes.zip", "33040", "900.48 KB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vt_all-records_codes.zip", "46532", "1.2 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vt_all-records_codes.zip", "32687", "942.34 KB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vt_all-records_codes.zip", "36637", "971.16 KB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vt_all-records_codes.zip", "32790", "897.96 KB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vt_all-records_codes.zip", "37869", "998.22 KB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_vt_originated-records_codes.zip",
                    "15176",
                    "399.34 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_vt_originated-records_codes.zip",
                    "20755",
                    "567.25 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_vt_originated-records_codes.zip",
                    "13325",
                    "283.84 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_vt_originated-records_codes.zip",
                    "14053",
                    "403.29 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_vt_originated-records_codes.zip",
                    "11893",
                    "311.95 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_vt_originated-records_codes.zip",
                    "17432",
                    "462.77 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_vt_originated-records_codes.zip",
                    "25699",
                    "638.61 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_vt_originated-records_codes.zip",
                    "17791",
                    "486.47 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_vt_originated-records_codes.zip",
                    "19808",
                    "497.91 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_vt_originated-records_codes.zip",
                    "19293",
                    "501.93 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_vt_originated-records_codes.zip",
                    "22745",
                    "561.59 KB",
                ),
            },
        },
    },
    "il": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_il_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "278035",
                    "14.02 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_il_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "346807",
                    "16.76 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_il_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "225445",
                    "7.03 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_il_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "245110",
                    "13.66 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_il_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "193991",
                    "9.89 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_il_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "278003",
                    "13.04 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_il_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "396141",
                    "17.05 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_il_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "282861",
                    "13.82 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_il_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "343779",
                    "16.76 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_il_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "295909",
                    "14.97 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_il_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "378550",
                    "18.82 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_il_all-records_labels.zip", "583019", "31.48 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_il_all-records_labels.zip",
                    "1117310",
                    "53.26 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_il_all-records_labels.zip", "502511", "18.63 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_il_all-records_labels.zip", "517360", "30.86 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_il_all-records_labels.zip", "437239", "23.79 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_il_all-records_labels.zip", "761632", "36.35 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_il_all-records_labels.zip", "849782", "37.88 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_il_all-records_labels.zip", "620832", "33.1 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_il_all-records_labels.zip", "716356", "37.81 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_il_all-records_labels.zip", "637258", "34.91 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_il_all-records_labels.zip", "754118", "40.71 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_il_originated-records_labels.zip",
                    "317597",
                    "16.17 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_il_originated-records_labels.zip",
                    "470592",
                    "22.68 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_il_originated-records_labels.zip",
                    "265490",
                    "8.51 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_il_originated-records_labels.zip",
                    "284551",
                    "16.06 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_il_originated-records_labels.zip",
                    "232557",
                    "11.98 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_il_originated-records_labels.zip",
                    "339543",
                    "16.11 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_il_originated-records_labels.zip",
                    "432707",
                    "18.86 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_il_originated-records_labels.zip",
                    "319004",
                    "15.78 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_il_originated-records_labels.zip",
                    "378335",
                    "18.65 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_il_originated-records_labels.zip",
                    "344172",
                    "17.61 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_il_originated-records_labels.zip",
                    "424748",
                    "21.38 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_il_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "278035",
                    "10.15 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_il_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "346807",
                    "12.31 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_il_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "225445",
                    "5.06 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_il_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "245110",
                    "9.83 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_il_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "193991",
                    "7.12 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_il_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "278003",
                    "9.54 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_il_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "396141",
                    "12.55 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_il_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "282861",
                    "9.82 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_il_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "343779",
                    "11.91 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_il_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "295909",
                    "10.83 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_il_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "378550",
                    "13.52 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_il_all-records_codes.zip", "583019", "22.25 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_il_all-records_codes.zip", "1117310", "37.59 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_il_all-records_codes.zip", "502511", "12.69 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_il_all-records_codes.zip", "517360", "21.34 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_il_all-records_codes.zip", "437239", "16.64 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_il_all-records_codes.zip", "761632", "25.64 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_il_all-records_codes.zip", "849782", "26.91 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_il_all-records_codes.zip", "620832", "22.91 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_il_all-records_codes.zip", "716356", "26.12 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_il_all-records_codes.zip", "637258", "24.68 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_il_all-records_codes.zip", "754118", "28.69 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_il_originated-records_codes.zip",
                    "317597",
                    "11.62 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_il_originated-records_codes.zip",
                    "470592",
                    "16.53 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_il_originated-records_codes.zip",
                    "265490",
                    "6.03 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_il_originated-records_codes.zip",
                    "284551",
                    "11.44 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_il_originated-records_codes.zip",
                    "232557",
                    "8.54 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_il_originated-records_codes.zip",
                    "339543",
                    "11.68 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_il_originated-records_codes.zip",
                    "432707",
                    "13.79 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_il_originated-records_codes.zip",
                    "319004",
                    "11.14 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_il_originated-records_codes.zip",
                    "378335",
                    "13.17 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_il_originated-records_codes.zip",
                    "344172",
                    "12.64 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_il_originated-records_codes.zip",
                    "424748",
                    "15.26 MB",
                ),
            },
        },
    },
    "ga": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ga_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "225258",
                    "11.78 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ga_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "236346",
                    "11.17 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ga_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "203948",
                    "6.37 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ga_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "193285",
                    "11.11 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ga_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "147432",
                    "7.81 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ga_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "179658",
                    "8.42 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ga_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "220141",
                    "9.84 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ga_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "165891",
                    "8.32 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ga_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "171421",
                    "8.49 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ga_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "210048",
                    "10.77 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ga_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "229259",
                    "11.67 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ga_all-records_labels.zip", "547637", "30.4 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ga_all-records_labels.zip", "899812", "43.49 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ga_all-records_labels.zip", "501310", "18.01 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ga_all-records_labels.zip", "478359", "29.23 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ga_all-records_labels.zip", "391231", "22.06 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ga_all-records_labels.zip", "583802", "28.24 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ga_all-records_labels.zip", "612188", "28.44 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ga_all-records_labels.zip", "444258", "24.51 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ga_all-records_labels.zip", "466839", "25.16 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ga_all-records_labels.zip", "537898", "29.53 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ga_all-records_labels.zip", "559464", "30.51 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ga_originated-records_labels.zip",
                    "264802",
                    "14.07 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ga_originated-records_labels.zip",
                    "352181",
                    "16.55 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ga_originated-records_labels.zip",
                    "244731",
                    "7.97 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ga_originated-records_labels.zip",
                    "232822",
                    "13.6 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ga_originated-records_labels.zip",
                    "185375",
                    "10 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ga_originated-records_labels.zip",
                    "244230",
                    "11.53 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ga_originated-records_labels.zip",
                    "261989",
                    "11.88 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ga_originated-records_labels.zip",
                    "204582",
                    "10.57 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ga_originated-records_labels.zip",
                    "208728",
                    "10.42 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ga_originated-records_labels.zip",
                    "262544",
                    "13.64 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ga_originated-records_labels.zip",
                    "277607",
                    "14.27 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ga_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "225258",
                    "8.23 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ga_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "236346",
                    "7.88 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ga_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "203948",
                    "4.43 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ga_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "193285",
                    "7.71 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ga_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "147432",
                    "5.46 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ga_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "179658",
                    "5.94 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ga_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "220141",
                    "7.02 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ga_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "165891",
                    "5.63 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ga_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "171421",
                    "5.76 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ga_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "210048",
                    "7.54 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ga_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "229259",
                    "8.16 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ga_all-records_codes.zip", "547637", "20.69 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ga_all-records_codes.zip", "899812", "29.71 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ga_all-records_codes.zip", "501310", "11.97 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ga_all-records_codes.zip", "478359", "19.47 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ga_all-records_codes.zip", "391231", "14.94 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ga_all-records_codes.zip", "583802", "19.31 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ga_all-records_codes.zip", "612188", "19.6 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ga_all-records_codes.zip", "444258", "16.2 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ga_all-records_codes.zip", "466839", "16.61 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ga_all-records_codes.zip", "537898", "20.11 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ga_all-records_codes.zip", "559464", "20.8 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ga_originated-records_codes.zip",
                    "264802",
                    "9.77 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ga_originated-records_codes.zip",
                    "352181",
                    "11.59 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ga_originated-records_codes.zip",
                    "244731",
                    "5.49 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ga_originated-records_codes.zip",
                    "232822",
                    "9.35 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ga_originated-records_codes.zip",
                    "185375",
                    "6.91 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ga_originated-records_codes.zip",
                    "244230",
                    "8.04 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ga_originated-records_codes.zip",
                    "261989",
                    "8.4 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ga_originated-records_codes.zip",
                    "204582",
                    "7.11 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ga_originated-records_codes.zip",
                    "208728",
                    "7.02 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ga_originated-records_codes.zip",
                    "262544",
                    "9.46 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ga_originated-records_codes.zip",
                    "277607",
                    "9.89 MB",
                ),
            },
        },
    },
    "in": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_in_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "149979",
                    "7.55 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_in_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "145394",
                    "6.8 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_in_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "135246",
                    "4.03 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_in_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "134522",
                    "7.59 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_in_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "108789",
                    "5.36 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_in_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "124555",
                    "5.73 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_in_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "187145",
                    "8.03 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_in_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "141707",
                    "6.73 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_in_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "161225",
                    "7.29 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_in_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "159649",
                    "7.66 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_in_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "188614",
                    "8.83 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_in_all-records_labels.zip", "319123", "17.64 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_in_all-records_labels.zip", "474561", "24.38 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_in_all-records_labels.zip", "292152", "10.14 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_in_all-records_labels.zip", "288746", "17.61 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_in_all-records_labels.zip", "248347", "13.51 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_in_all-records_labels.zip", "348681", "17.43 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_in_all-records_labels.zip", "421392", "19.89 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_in_all-records_labels.zip", "322061", "17.24 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_in_all-records_labels.zip", "359860", "18.65 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_in_all-records_labels.zip", "344116", "18.48 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_in_all-records_labels.zip", "385267", "20.36 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_in_originated-records_labels.zip",
                    "172307",
                    "8.79 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_in_originated-records_labels.zip",
                    "199213",
                    "9.38 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_in_originated-records_labels.zip",
                    "158693",
                    "4.9 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_in_originated-records_labels.zip",
                    "156109",
                    "8.92 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_in_originated-records_labels.zip",
                    "130131",
                    "6.52 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_in_originated-records_labels.zip",
                    "155308",
                    "7.25 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_in_originated-records_labels.zip",
                    "207593",
                    "9.02 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_in_originated-records_labels.zip",
                    "160424",
                    "7.77 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_in_originated-records_labels.zip",
                    "179820",
                    "8.27 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_in_originated-records_labels.zip",
                    "184428",
                    "8.97 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_in_originated-records_labels.zip",
                    "210891",
                    "10.05 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_in_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "149979",
                    "5.05 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_in_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "145394",
                    "4.63 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_in_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "135246",
                    "2.85 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_in_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "134522",
                    "5.11 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_in_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "108789",
                    "3.62 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_in_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "124555",
                    "3.9 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_in_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "187145",
                    "5.67 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_in_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "141707",
                    "4.43 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_in_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "161225",
                    "4.82 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_in_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "159649",
                    "5.11 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_in_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "188614",
                    "5.87 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_in_all-records_codes.zip", "319123", "11.54 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_in_all-records_codes.zip", "474561", "16.44 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_in_all-records_codes.zip", "292152", "6.68 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_in_all-records_codes.zip", "288746", "11.46 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_in_all-records_codes.zip", "248347", "8.9 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_in_all-records_codes.zip", "348681", "11.68 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_in_all-records_codes.zip", "421392", "13.64 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_in_all-records_codes.zip", "322061", "11.1 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_in_all-records_codes.zip", "359860", "12.06 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_in_all-records_codes.zip", "344116", "12.12 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_in_all-records_codes.zip", "385267", "13.31 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_in_originated-records_codes.zip",
                    "172307",
                    "5.84 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_in_originated-records_codes.zip",
                    "199213",
                    "6.61 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_in_originated-records_codes.zip",
                    "158693",
                    "3.43 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_in_originated-records_codes.zip",
                    "156109",
                    "5.98 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_in_originated-records_codes.zip",
                    "130131",
                    "4.37 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_in_originated-records_codes.zip",
                    "155308",
                    "4.94 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_in_originated-records_codes.zip",
                    "207593",
                    "6.34 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_in_originated-records_codes.zip",
                    "160424",
                    "5.09 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_in_originated-records_codes.zip",
                    "179820",
                    "5.44 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_in_originated-records_codes.zip",
                    "184428",
                    "5.94 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_in_originated-records_codes.zip",
                    "210891",
                    "6.64 MB",
                ),
            },
        },
    },
    "ia": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ia_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "71680",
                    "3.32 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ia_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "65703",
                    "3.02 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ia_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "60347",
                    "1.83 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ia_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "63773",
                    "3.32 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ia_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "52784",
                    "2.39 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ia_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "60097",
                    "2.72 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ia_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "96858",
                    "3.85 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ia_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "72565",
                    "3.17 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ia_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "84923",
                    "3.79 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ia_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "76061",
                    "3.38 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ia_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "93906",
                    "4.12 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ia_all-records_labels.zip", "149227", "7.39 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ia_all-records_labels.zip", "197991", "9.31 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ia_all-records_labels.zip", "127446", "4.12 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ia_all-records_labels.zip", "136795", "7.68 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ia_all-records_labels.zip", "115594", "5.62 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ia_all-records_labels.zip", "157339", "7.52 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ia_all-records_labels.zip", "200497", "8.54 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ia_all-records_labels.zip", "150683", "7.18 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ia_all-records_labels.zip", "172100", "8.41 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ia_all-records_labels.zip", "160707", "7.67 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ia_all-records_labels.zip", "181237", "8.53 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ia_originated-records_labels.zip",
                    "90932",
                    "4.27 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ia_originated-records_labels.zip",
                    "93343",
                    "4.31 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ia_originated-records_labels.zip",
                    "79977",
                    "2.43 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ia_originated-records_labels.zip",
                    "83214",
                    "4.37 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ia_originated-records_labels.zip",
                    "71413",
                    "3.26 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ia_originated-records_labels.zip",
                    "78965",
                    "3.63 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ia_originated-records_labels.zip",
                    "112522",
                    "4.57 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ia_originated-records_labels.zip",
                    "87178",
                    "3.88 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ia_originated-records_labels.zip",
                    "100132",
                    "4.56 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ia_originated-records_labels.zip",
                    "95886",
                    "4.34 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ia_originated-records_labels.zip",
                    "111610",
                    "4.98 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ia_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "71680",
                    "2.17 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ia_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "65703",
                    "2.02 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ia_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "60347",
                    "1.29 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ia_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "63773",
                    "2.2 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ia_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "52784",
                    "1.56 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ia_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "60097",
                    "1.82 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ia_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "96858",
                    "2.64 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ia_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "72565",
                    "2.05 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ia_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "84923",
                    "2.46 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ia_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "76061",
                    "2.18 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ia_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "93906",
                    "2.66 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ia_all-records_codes.zip", "149227", "4.65 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ia_all-records_codes.zip", "197991", "6.1 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ia_all-records_codes.zip", "127446", "2.7 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ia_all-records_codes.zip", "136795", "4.9 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ia_all-records_codes.zip", "115594", "3.51 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ia_all-records_codes.zip", "157339", "4.92 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ia_all-records_codes.zip", "200497", "5.67 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ia_all-records_codes.zip", "150683", "4.49 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ia_all-records_codes.zip", "172100", "5.28 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ia_all-records_codes.zip", "160707", "4.75 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ia_all-records_codes.zip", "181237", "5.31 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ia_originated-records_codes.zip",
                    "90932",
                    "2.74 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ia_originated-records_codes.zip",
                    "93343",
                    "2.86 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ia_originated-records_codes.zip",
                    "79977",
                    "1.67 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ia_originated-records_codes.zip",
                    "83214",
                    "2.85 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ia_originated-records_codes.zip",
                    "71413",
                    "2.08 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ia_originated-records_codes.zip",
                    "78965",
                    "2.41 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ia_originated-records_codes.zip",
                    "112522",
                    "3.11 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ia_originated-records_codes.zip",
                    "87178",
                    "2.48 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ia_originated-records_codes.zip",
                    "100132",
                    "2.93 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ia_originated-records_codes.zip",
                    "95886",
                    "2.76 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ia_originated-records_codes.zip",
                    "111610",
                    "3.18 MB",
                ),
            },
        },
    },
    "az": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_az_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "201543",
                    "9.98 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_az_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "198791",
                    "8.9 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_az_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "177849",
                    "5.45 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_az_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "166410",
                    "8.87 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_az_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "124580",
                    "6.3 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_az_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "129343",
                    "5.73 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_az_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "161393",
                    "6.71 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_az_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "114583",
                    "5.41 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_az_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "132138",
                    "6.21 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_az_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "176268",
                    "8.6 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_az_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "197491",
                    "9.59 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_az_all-records_labels.zip", "478386", "24.75 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_az_all-records_labels.zip", "803675", "35.11 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_az_all-records_labels.zip", "428411", "14.46 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_az_all-records_labels.zip", "391879", "22 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_az_all-records_labels.zip", "317345", "16.74 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_az_all-records_labels.zip", "425680", "19.23 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_az_all-records_labels.zip", "441291", "18.88 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_az_all-records_labels.zip", "313348", "16.05 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_az_all-records_labels.zip", "350571", "17.93 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_az_all-records_labels.zip", "428383", "22.29 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_az_all-records_labels.zip", "458365", "23.72 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_az_originated-records_labels.zip",
                    "236688",
                    "11.85 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_az_originated-records_labels.zip",
                    "292272",
                    "13.05 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_az_originated-records_labels.zip",
                    "213547",
                    "6.63 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_az_originated-records_labels.zip",
                    "198908",
                    "10.8 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_az_originated-records_labels.zip",
                    "155001",
                    "7.95 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_az_originated-records_labels.zip",
                    "165011",
                    "7.37 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_az_originated-records_labels.zip",
                    "190609",
                    "7.98 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_az_originated-records_labels.zip",
                    "146231",
                    "7.09 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_az_originated-records_labels.zip",
                    "160055",
                    "7.73 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_az_originated-records_labels.zip",
                    "224986",
                    "11.14 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_az_originated-records_labels.zip",
                    "247572",
                    "12.19 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_az_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "201543",
                    "7.26 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_az_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "198791",
                    "6.42 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_az_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "177849",
                    "3.82 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_az_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "166410",
                    "6.44 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_az_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "124580",
                    "4.59 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_az_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "129343",
                    "4.15 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_az_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "161393",
                    "4.89 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_az_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "114583",
                    "3.79 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_az_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "132138",
                    "4.33 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_az_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "176268",
                    "6.24 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_az_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "197491",
                    "6.92 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_az_all-records_codes.zip", "478386", "17.45 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_az_all-records_codes.zip", "803675", "24.35 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_az_all-records_codes.zip", "428411", "9.68 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_az_all-records_codes.zip", "391879", "15.26 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_az_all-records_codes.zip", "317345", "11.78 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_az_all-records_codes.zip", "425680", "13.42 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_az_all-records_codes.zip", "441291", "13.49 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_az_all-records_codes.zip", "313348", "10.91 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_az_all-records_codes.zip", "350571", "12.17 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_az_all-records_codes.zip", "428383", "15.68 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_az_all-records_codes.zip", "458365", "16.67 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_az_originated-records_codes.zip",
                    "236688",
                    "8.56 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_az_originated-records_codes.zip",
                    "292272",
                    "9.39 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_az_originated-records_codes.zip",
                    "213547",
                    "4.61 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_az_originated-records_codes.zip",
                    "198908",
                    "7.79 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_az_originated-records_codes.zip",
                    "155001",
                    "5.74 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_az_originated-records_codes.zip",
                    "165011",
                    "5.32 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_az_originated-records_codes.zip",
                    "190609",
                    "5.81 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_az_originated-records_codes.zip",
                    "146231",
                    "4.94 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_az_originated-records_codes.zip",
                    "160055",
                    "5.38 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_az_originated-records_codes.zip",
                    "224986",
                    "8.02 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_az_originated-records_codes.zip",
                    "247572",
                    "8.75 MB",
                ),
            },
        },
    },
    "id": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_id_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "49270",
                    "2.03 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_id_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "45546",
                    "1.84 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_id_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "43374",
                    "1.27 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_id_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "41252",
                    "1.97 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_id_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "30539",
                    "1.29 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_id_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "36308",
                    "1.49 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_id_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "49056",
                    "1.87 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_id_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "30665",
                    "1.26 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_id_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "37182",
                    "1.47 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_id_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "41770",
                    "1.75 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_id_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "46607",
                    "1.91 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_id_all-records_labels.zip", "103880", "4.67 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_id_all-records_labels.zip", "156706", "6.54 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_id_all-records_labels.zip", "92755", "3.01 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_id_all-records_labels.zip", "89063", "4.72 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_id_all-records_labels.zip", "70222", "3.27 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_id_all-records_labels.zip", "108689", "4.65 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_id_all-records_labels.zip", "125244", "5.05 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_id_all-records_labels.zip", "77672", "3.5 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_id_all-records_labels.zip", "94170", "4.16 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_id_all-records_labels.zip", "97051", "4.49 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_id_all-records_labels.zip", "103766", "4.64 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_id_originated-records_labels.zip",
                    "59151",
                    "2.48 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_id_originated-records_labels.zip",
                    "67396",
                    "2.74 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_id_originated-records_labels.zip",
                    "54102",
                    "1.62 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_id_originated-records_labels.zip",
                    "50554",
                    "2.46 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_id_originated-records_labels.zip",
                    "38605",
                    "1.67 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_id_originated-records_labels.zip",
                    "46531",
                    "1.93 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_id_originated-records_labels.zip",
                    "56985",
                    "2.2 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_id_originated-records_labels.zip",
                    "37943",
                    "1.6 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_id_originated-records_labels.zip",
                    "44663",
                    "1.79 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_id_originated-records_labels.zip",
                    "53109",
                    "2.27 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_id_originated-records_labels.zip",
                    "57188",
                    "2.39 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_id_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "49270",
                    "1.31 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_id_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "45546",
                    "1.22 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_id_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "43374",
                    "882.08 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_id_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "41252",
                    "1.28 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_id_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "30539",
                    "834.4 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_id_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "36308",
                    "1 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_id_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "49056",
                    "1.27 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_id_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "30665",
                    "802.44 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_id_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "37182",
                    "944.45 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_id_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "41770",
                    "1.12 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_id_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "46607",
                    "1.21 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_id_all-records_codes.zip", "103880", "2.88 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_id_all-records_codes.zip", "156706", "4.26 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_id_all-records_codes.zip", "92755", "1.96 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_id_all-records_codes.zip", "89063", "2.95 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_id_all-records_codes.zip", "70222", "2.02 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_id_all-records_codes.zip", "108689", "3.03 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_id_all-records_codes.zip", "125244", "3.33 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_id_all-records_codes.zip", "77672", "2.17 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_id_all-records_codes.zip", "94170", "2.57 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_id_all-records_codes.zip", "97051", "2.76 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_id_all-records_codes.zip", "103766", "2.85 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_id_originated-records_codes.zip",
                    "59151",
                    "1.59 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_id_originated-records_codes.zip",
                    "67396",
                    "1.83 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_id_originated-records_codes.zip",
                    "54102",
                    "1.11 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_id_originated-records_codes.zip",
                    "50554",
                    "1.59 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_id_originated-records_codes.zip",
                    "38605",
                    "1.07 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_id_originated-records_codes.zip",
                    "46531",
                    "1.29 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_id_originated-records_codes.zip",
                    "56985",
                    "1.49 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_id_originated-records_codes.zip",
                    "37943",
                    "1.02 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_id_originated-records_codes.zip",
                    "44663",
                    "1.14 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_id_originated-records_codes.zip",
                    "53109",
                    "1.45 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_id_originated-records_codes.zip",
                    "57188",
                    "1.51 MB",
                ),
            },
        },
    },
    "ct": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ct_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "66025",
                    "3.2 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ct_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "89152",
                    "4.26 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ct_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "57398",
                    "1.83 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ct_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "59656",
                    "3.12 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ct_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "49553",
                    "2.54 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ct_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "68658",
                    "3.22 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ct_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "104310",
                    "4.56 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ct_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "78978",
                    "3.93 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ct_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "93797",
                    "4.54 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ct_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "87390",
                    "4.18 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ct_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "105049",
                    "4.95 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ct_all-records_labels.zip", "146885", "7.73 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ct_all-records_labels.zip", "301760", "15.1 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ct_all-records_labels.zip", "129401", "4.77 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ct_all-records_labels.zip", "132491", "7.44 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ct_all-records_labels.zip", "114931", "6.31 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ct_all-records_labels.zip", "193168", "9.76 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ct_all-records_labels.zip", "235997", "11.17 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ct_all-records_labels.zip", "177460", "9.5 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ct_all-records_labels.zip", "204936", "10.79 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ct_all-records_labels.zip", "187158", "9.86 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ct_all-records_labels.zip", "214191", "11.09 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ct_originated-records_labels.zip",
                    "75239",
                    "3.73 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ct_originated-records_labels.zip",
                    "126259",
                    "6.09 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ct_originated-records_labels.zip",
                    "67000",
                    "2.19 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ct_originated-records_labels.zip",
                    "68865",
                    "3.65 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ct_originated-records_labels.zip",
                    "58456",
                    "3.04 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ct_originated-records_labels.zip",
                    "84484",
                    "4.01 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ct_originated-records_labels.zip",
                    "113317",
                    "5.04 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ct_originated-records_labels.zip",
                    "87795",
                    "4.47 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ct_originated-records_labels.zip",
                    "102545",
                    "5.08 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ct_originated-records_labels.zip",
                    "98739",
                    "4.8 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ct_originated-records_labels.zip",
                    "115361",
                    "5.49 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ct_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "66025",
                    "2.19 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ct_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "89152",
                    "2.98 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ct_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "57398",
                    "1.3 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ct_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "59656",
                    "2.2 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ct_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "49553",
                    "1.74 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ct_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "68658",
                    "2.25 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ct_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "104310",
                    "3.22 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ct_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "78978",
                    "2.66 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ct_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "93797",
                    "3.09 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ct_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "87390",
                    "2.84 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ct_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "105049",
                    "3.31 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ct_all-records_codes.zip", "146885", "5.17 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ct_all-records_codes.zip", "301760", "10.45 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ct_all-records_codes.zip", "129401", "3.24 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ct_all-records_codes.zip", "132491", "5.05 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ct_all-records_codes.zip", "114931", "4.22 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ct_all-records_codes.zip", "193168", "6.73 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ct_all-records_codes.zip", "235997", "7.73 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ct_all-records_codes.zip", "177460", "6.28 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ct_all-records_codes.zip", "204936", "7.18 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ct_all-records_codes.zip", "187158", "6.56 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ct_all-records_codes.zip", "214191", "7.31 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ct_originated-records_codes.zip",
                    "75239",
                    "2.54 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ct_originated-records_codes.zip",
                    "126259",
                    "4.28 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ct_originated-records_codes.zip",
                    "67000",
                    "1.55 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ct_originated-records_codes.zip",
                    "68865",
                    "2.57 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ct_originated-records_codes.zip",
                    "58456",
                    "2.07 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ct_originated-records_codes.zip",
                    "84484",
                    "2.79 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ct_originated-records_codes.zip",
                    "113317",
                    "3.55 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ct_originated-records_codes.zip",
                    "87795",
                    "3.04 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ct_originated-records_codes.zip",
                    "102545",
                    "3.46 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ct_originated-records_codes.zip",
                    "98739",
                    "3.24 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ct_originated-records_codes.zip",
                    "115361",
                    "3.66 MB",
                ),
            },
        },
    },
    "nh": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "32293",
                    "1.45 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "30786",
                    "1.35 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "28246",
                    "825.86 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "27470",
                    "1.33 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "21418",
                    "953.08 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "25186",
                    "1.1 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "40099",
                    "1.65 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "30214",
                    "1.28 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "35463",
                    "1.49 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "34908",
                    "1.55 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "41909",
                    "1.8 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nh_all-records_labels.zip", "72628", "3.51 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nh_all-records_labels.zip", "116500", "5.13 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nh_all-records_labels.zip", "65016", "2 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nh_all-records_labels.zip", "63482", "3.36 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nh_all-records_labels.zip", "53373", "2.55 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nh_all-records_labels.zip", "78591", "3.53 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nh_all-records_labels.zip", "100680", "4.29 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nh_all-records_labels.zip", "75090", "3.48 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nh_all-records_labels.zip", "85990", "3.93 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nh_all-records_labels.zip", "80737", "3.88 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nh_all-records_labels.zip", "92574", "4.33 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nh_originated-records_labels.zip",
                    "38262",
                    "1.76 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nh_originated-records_labels.zip",
                    "46139",
                    "2.02 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nh_originated-records_labels.zip",
                    "34290",
                    "1.02 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nh_originated-records_labels.zip",
                    "33120",
                    "1.64 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nh_originated-records_labels.zip",
                    "26589",
                    "1.21 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nh_originated-records_labels.zip",
                    "32850",
                    "1.46 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nh_originated-records_labels.zip",
                    "45790",
                    "1.91 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nh_originated-records_labels.zip",
                    "35321",
                    "1.53 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nh_originated-records_labels.zip",
                    "40696",
                    "1.75 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nh_originated-records_labels.zip",
                    "41589",
                    "1.88 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nh_originated-records_labels.zip",
                    "48098",
                    "2.12 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "32293",
                    "929.81 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "30786",
                    "870.93 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "28246",
                    "579.48 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "27470",
                    "880.79 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "21418",
                    "605.7 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "25186",
                    "724.38 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "40099",
                    "1.1 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "30214",
                    "801.84 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "35463",
                    "934.66 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "34908",
                    "991.18 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "41909",
                    "1.14 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nh_all-records_codes.zip", "72628", "2.16 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nh_all-records_codes.zip", "116500", "3.28 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nh_all-records_codes.zip", "65016", "1.3 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nh_all-records_codes.zip", "63482", "2.15 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nh_all-records_codes.zip", "53373", "1.56 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nh_all-records_codes.zip", "78591", "2.27 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nh_all-records_codes.zip", "100680", "2.81 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nh_all-records_codes.zip", "75090", "2.12 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nh_all-records_codes.zip", "85990", "2.4 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nh_all-records_codes.zip", "80737", "2.4 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nh_all-records_codes.zip", "92574", "2.66 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nh_originated-records_codes.zip",
                    "38262",
                    "1.12 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nh_originated-records_codes.zip",
                    "46139",
                    "1.31 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nh_originated-records_codes.zip",
                    "34290",
                    "702.18 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nh_originated-records_codes.zip",
                    "33120",
                    "1.08 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nh_originated-records_codes.zip",
                    "26589",
                    "760.91 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nh_originated-records_codes.zip",
                    "32850",
                    "959.54 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nh_originated-records_codes.zip",
                    "45790",
                    "1.27 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nh_originated-records_codes.zip",
                    "35321",
                    "955.91 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nh_originated-records_codes.zip",
                    "40696",
                    "1.09 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nh_originated-records_codes.zip",
                    "41589",
                    "1.2 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nh_originated-records_codes.zip",
                    "48098",
                    "1.33 MB",
                ),
            },
        },
    },
    "nj": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nj_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "168437",
                    "8.44 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nj_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "222771",
                    "10.95 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nj_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "141365",
                    "4.57 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nj_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "147544",
                    "8.22 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nj_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "113481",
                    "5.78 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nj_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "166597",
                    "8.06 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nj_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "247580",
                    "11.18 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nj_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "184520",
                    "9.28 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nj_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "206564",
                    "10.4 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nj_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "194532",
                    "9.73 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nj_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "237169",
                    "11.87 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nj_all-records_labels.zip", "399389", "21.26 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nj_all-records_labels.zip", "808103", "39.11 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nj_all-records_labels.zip", "349563", "12.38 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nj_all-records_labels.zip", "354746", "21.29 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nj_all-records_labels.zip", "289377", "15.65 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nj_all-records_labels.zip", "514816", "25.05 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nj_all-records_labels.zip", "613066", "28.18 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nj_all-records_labels.zip", "451221", "24.28 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nj_all-records_labels.zip", "499489", "27 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nj_all-records_labels.zip", "460264", "24.64 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nj_all-records_labels.zip", "541802", "29.13 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nj_originated-records_labels.zip",
                    "194913",
                    "9.86 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nj_originated-records_labels.zip",
                    "317276",
                    "15.57 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nj_originated-records_labels.zip",
                    "169196",
                    "5.6 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nj_originated-records_labels.zip",
                    "171685",
                    "9.68 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nj_originated-records_labels.zip",
                    "135675",
                    "6.98 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nj_originated-records_labels.zip",
                    "208721",
                    "10.17 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nj_originated-records_labels.zip",
                    "274489",
                    "12.53 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nj_originated-records_labels.zip",
                    "210948",
                    "10.71 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nj_originated-records_labels.zip",
                    "232001",
                    "11.8 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nj_originated-records_labels.zip",
                    "226181",
                    "11.43 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nj_originated-records_labels.zip",
                    "269377",
                    "13.64 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nj_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "168437",
                    "6.08 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nj_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "222771",
                    "7.81 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nj_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "141365",
                    "3.22 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nj_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "147544",
                    "5.93 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nj_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "113481",
                    "4.17 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nj_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "166597",
                    "5.77 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nj_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "247580",
                    "8.06 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nj_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "184520",
                    "6.49 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nj_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "206564",
                    "7.36 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nj_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "194532",
                    "6.89 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nj_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "237169",
                    "8.4 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nj_all-records_codes.zip", "399389", "14.78 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nj_all-records_codes.zip", "808103", "27.04 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nj_all-records_codes.zip", "349563", "8.1 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nj_all-records_codes.zip", "354746", "14.72 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nj_all-records_codes.zip", "289377", "10.83 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nj_all-records_codes.zip", "514816", "17.43 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nj_all-records_codes.zip", "613066", "19.76 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nj_all-records_codes.zip", "451221", "16.47 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nj_all-records_codes.zip", "499489", "18.44 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nj_all-records_codes.zip", "460264", "16.86 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nj_all-records_codes.zip", "541802", "19.93 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nj_originated-records_codes.zip",
                    "194913",
                    "7.06 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nj_originated-records_codes.zip",
                    "317276",
                    "11.05 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nj_originated-records_codes.zip",
                    "169196",
                    "3.91 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nj_originated-records_codes.zip",
                    "171685",
                    "6.93 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nj_originated-records_codes.zip",
                    "135675",
                    "5 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nj_originated-records_codes.zip",
                    "208721",
                    "7.24 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nj_originated-records_codes.zip",
                    "274489",
                    "9.01 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nj_originated-records_codes.zip",
                    "210948",
                    "7.44 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nj_originated-records_codes.zip",
                    "232001",
                    "8.28 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nj_originated-records_codes.zip",
                    "226181",
                    "8.05 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nj_originated-records_codes.zip",
                    "269377",
                    "9.59 MB",
                ),
            },
        },
    },
    "nm": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nm_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "32653",
                    "1.47 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nm_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "47002",
                    "2.07 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nm_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "28982",
                    "924.59 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nm_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "29038",
                    "1.45 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nm_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "24491",
                    "1.13 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nm_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "35421",
                    "1.54 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nm_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "45147",
                    "1.83 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nm_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "31586",
                    "1.35 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nm_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "36691",
                    "1.68 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nm_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "38141",
                    "1.77 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nm_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "42629",
                    "1.91 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nm_all-records_labels.zip", "89390", "4.48 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nm_all-records_labels.zip", "178911", "8.19 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nm_all-records_labels.zip", "80423", "2.86 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nm_all-records_labels.zip", "79236", "4.37 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nm_all-records_labels.zip", "71841", "3.67 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nm_all-records_labels.zip", "114678", "5.3 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nm_all-records_labels.zip", "123495", "5.37 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nm_all-records_labels.zip", "90785", "4.39 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nm_all-records_labels.zip", "104045", "5.33 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nm_all-records_labels.zip", "102217", "5.23 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nm_all-records_labels.zip", "108074", "5.4 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nm_originated-records_labels.zip",
                    "41334",
                    "1.93 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nm_originated-records_labels.zip",
                    "69876",
                    "3.15 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nm_originated-records_labels.zip",
                    "37465",
                    "1.24 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nm_originated-records_labels.zip",
                    "37572",
                    "1.93 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nm_originated-records_labels.zip",
                    "32547",
                    "1.57 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nm_originated-records_labels.zip",
                    "46512",
                    "2.09 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nm_originated-records_labels.zip",
                    "54007",
                    "2.27 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nm_originated-records_labels.zip",
                    "39979",
                    "1.8 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nm_originated-records_labels.zip",
                    "45261",
                    "2.12 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nm_originated-records_labels.zip",
                    "49389",
                    "2.34 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nm_originated-records_labels.zip",
                    "53038",
                    "2.41 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nm_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "32653",
                    "980.97 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nm_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "47002",
                    "1.42 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nm_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "28982",
                    "644.64 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nm_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "29038",
                    "989.53 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nm_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "24491",
                    "759.74 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nm_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "35421",
                    "1.05 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nm_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "45147",
                    "1.26 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nm_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "31586",
                    "892.04 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nm_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "36691",
                    "1.12 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nm_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "38141",
                    "1.18 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nm_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "42629",
                    "1.26 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nm_all-records_codes.zip", "89390", "2.89 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nm_all-records_codes.zip", "178911", "5.48 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nm_all-records_codes.zip", "80423", "1.88 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nm_all-records_codes.zip", "79236", "2.87 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nm_all-records_codes.zip", "71841", "2.38 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nm_all-records_codes.zip", "114678", "3.55 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nm_all-records_codes.zip", "123495", "3.6 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nm_all-records_codes.zip", "90785", "2.81 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nm_all-records_codes.zip", "104045", "3.42 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nm_all-records_codes.zip", "102217", "3.39 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nm_all-records_codes.zip", "108074", "3.48 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nm_originated-records_codes.zip",
                    "41334",
                    "1.3 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nm_originated-records_codes.zip",
                    "69876",
                    "2.15 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nm_originated-records_codes.zip",
                    "37465",
                    "864.54 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nm_originated-records_codes.zip",
                    "37572",
                    "1.32 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nm_originated-records_codes.zip",
                    "32547",
                    "1.05 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nm_originated-records_codes.zip",
                    "46512",
                    "1.43 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nm_originated-records_codes.zip",
                    "54007",
                    "1.56 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nm_originated-records_codes.zip",
                    "39979",
                    "1.19 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nm_originated-records_codes.zip",
                    "45261",
                    "1.4 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nm_originated-records_codes.zip",
                    "49389",
                    "1.56 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nm_originated-records_codes.zip",
                    "53038",
                    "1.59 MB",
                ),
            },
        },
    },
    "tx": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tx_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "513200",
                    "26.59 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tx_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "454756",
                    "22.34 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tx_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "457884",
                    "15.35 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tx_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "460596",
                    "26.85 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tx_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "391921",
                    "20.38 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tx_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "364311",
                    "17.57 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tx_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "448222",
                    "20.5 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tx_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "391184",
                    "19.56 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tx_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "405050",
                    "20.17 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tx_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "503627",
                    "26.39 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tx_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "502655",
                    "26.28 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tx_all-records_labels.zip",
                    "1266767",
                    "70.12 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tx_all-records_labels.zip",
                    "1723576",
                    "83.63 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tx_all-records_labels.zip",
                    "1148206",
                    "42.77 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tx_all-records_labels.zip",
                    "1139573",
                    "71.35 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tx_all-records_labels.zip",
                    "1011598",
                    "55.94 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tx_all-records_labels.zip",
                    "1204457",
                    "58.59 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tx_all-records_labels.zip",
                    "1242037",
                    "57.86 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tx_all-records_labels.zip",
                    "1038591",
                    "56.64 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tx_all-records_labels.zip",
                    "1063486",
                    "58.04 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tx_all-records_labels.zip", "1254738", "70.8 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tx_all-records_labels.zip",
                    "1221801",
                    "69.13 MB",
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tx_originated-records_labels.zip",
                    "613325",
                    "32.57 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tx_originated-records_labels.zip",
                    "653817",
                    "32.47 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tx_originated-records_labels.zip",
                    "559492",
                    "19.3 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tx_originated-records_labels.zip",
                    "557266",
                    "33.01 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tx_originated-records_labels.zip",
                    "484747",
                    "25.75 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tx_originated-records_labels.zip",
                    "473701",
                    "23.41 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tx_originated-records_labels.zip",
                    "520422",
                    "24.41 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tx_originated-records_labels.zip",
                    "466338",
                    "24 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tx_originated-records_labels.zip",
                    "476566",
                    "24.45 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tx_originated-records_labels.zip",
                    "611180",
                    "32.38 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tx_originated-records_labels.zip",
                    "594151",
                    "31.5 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tx_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "513200",
                    "18.9 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tx_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "454756",
                    "16.07 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tx_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "457884",
                    "10.67 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tx_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "460596",
                    "19.03 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tx_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "391921",
                    "14.47 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tx_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "364311",
                    "12.62 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tx_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "448222",
                    "14.81 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tx_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "391184",
                    "13.52 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tx_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "405050",
                    "13.93 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tx_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "503627",
                    "18.83 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tx_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "502655",
                    "18.62 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tx_all-records_codes.zip", "1266767", "48.14 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tx_all-records_codes.zip", "1723576", "58.17 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tx_all-records_codes.zip", "1148206", "27.41 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tx_all-records_codes.zip", "1139573", "48.5 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tx_all-records_codes.zip", "1011598", "38.26 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tx_all-records_codes.zip", "1204457", "40.77 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tx_all-records_codes.zip", "1242037", "40.49 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tx_all-records_codes.zip", "1038591", "38.13 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tx_all-records_codes.zip", "1063486", "39.1 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tx_all-records_codes.zip", "1254738", "48.99 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tx_all-records_codes.zip", "1221801", "47.68 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tx_originated-records_codes.zip",
                    "613325",
                    "23.08 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tx_originated-records_codes.zip",
                    "653817",
                    "23.29 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tx_originated-records_codes.zip",
                    "559492",
                    "13.3 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tx_originated-records_codes.zip",
                    "557266",
                    "23.23 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tx_originated-records_codes.zip",
                    "484747",
                    "18.19 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tx_originated-records_codes.zip",
                    "473701",
                    "16.77 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tx_originated-records_codes.zip",
                    "520422",
                    "17.57 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tx_originated-records_codes.zip",
                    "466338",
                    "16.56 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tx_originated-records_codes.zip",
                    "476566",
                    "16.85 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tx_originated-records_codes.zip",
                    "611180",
                    "22.91 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tx_originated-records_codes.zip",
                    "594151",
                    "22.16 MB",
                ),
            },
        },
    },
    "la": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_la_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "72627",
                    "3.46 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_la_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "86710",
                    "4.14 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_la_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "61729",
                    "1.89 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_la_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "67942",
                    "3.69 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_la_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "59398",
                    "2.86 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_la_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "69191",
                    "3.26 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_la_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "81760",
                    "3.74 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_la_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "69735",
                    "3.2 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_la_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "75645",
                    "3.55 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_la_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "77713",
                    "3.68 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_la_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "86148",
                    "4.02 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_la_all-records_labels.zip", "195937", "10.16 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_la_all-records_labels.zip", "300738", "14.74 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_la_all-records_labels.zip", "173079", "6.06 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_la_all-records_labels.zip", "180533", "10.55 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_la_all-records_labels.zip", "170514", "8.9 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_la_all-records_labels.zip", "221773", "11.04 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_la_all-records_labels.zip", "231242", "11.32 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_la_all-records_labels.zip", "210644", "10.99 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_la_all-records_labels.zip", "214403", "11.27 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_la_all-records_labels.zip", "219546", "11.6 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_la_all-records_labels.zip", "231946", "12.12 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_la_originated-records_labels.zip",
                    "94261",
                    "4.64 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_la_originated-records_labels.zip",
                    "126278",
                    "6.16 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_la_originated-records_labels.zip",
                    "83323",
                    "2.62 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_la_originated-records_labels.zip",
                    "89327",
                    "4.95 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_la_originated-records_labels.zip",
                    "81230",
                    "4.06 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_la_originated-records_labels.zip",
                    "97778",
                    "4.77 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_la_originated-records_labels.zip",
                    "103928",
                    "4.89 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_la_originated-records_labels.zip",
                    "90349",
                    "4.38 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_la_originated-records_labels.zip",
                    "96150",
                    "4.64 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_la_originated-records_labels.zip",
                    "101849",
                    "4.89 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_la_originated-records_labels.zip",
                    "107636",
                    "5.1 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_la_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "72627",
                    "2.33 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_la_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "86710",
                    "2.79 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_la_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "61729",
                    "1.36 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_la_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "67942",
                    "2.53 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_la_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "59398",
                    "1.93 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_la_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "69191",
                    "2.23 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_la_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "81760",
                    "2.59 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_la_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "69735",
                    "2.12 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_la_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "75645",
                    "2.36 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_la_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "77713",
                    "2.44 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_la_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "86148",
                    "2.66 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_la_all-records_codes.zip", "195937", "6.65 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_la_all-records_codes.zip", "300738", "9.84 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_la_all-records_codes.zip", "173079", "4 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_la_all-records_codes.zip", "180533", "6.97 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_la_all-records_codes.zip", "170514", "5.81 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_la_all-records_codes.zip", "221773", "7.43 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_la_all-records_codes.zip", "231242", "7.74 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_la_all-records_codes.zip", "210644", "7.15 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_la_all-records_codes.zip", "214403", "7.36 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_la_all-records_codes.zip", "219546", "7.57 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_la_all-records_codes.zip", "231946", "7.91 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_la_originated-records_codes.zip",
                    "94261",
                    "3.12 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_la_originated-records_codes.zip",
                    "126278",
                    "4.18 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_la_originated-records_codes.zip",
                    "83323",
                    "1.86 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_la_originated-records_codes.zip",
                    "89327",
                    "3.37 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_la_originated-records_codes.zip",
                    "81230",
                    "2.72 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_la_originated-records_codes.zip",
                    "97778",
                    "3.29 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_la_originated-records_codes.zip",
                    "103928",
                    "3.38 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_la_originated-records_codes.zip",
                    "90349",
                    "2.9 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_la_originated-records_codes.zip",
                    "96150",
                    "3.06 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_la_originated-records_codes.zip",
                    "101849",
                    "3.22 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_la_originated-records_codes.zip",
                    "107636",
                    "3.34 MB",
                ),
            },
        },
    },
    "wa": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "225231",
                    "11.2 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "215619",
                    "10.08 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "191532",
                    "6.03 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "183367",
                    "10.31 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "133913",
                    "6.66 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "165363",
                    "7.57 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "255387",
                    "10.98 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "174449",
                    "8.42 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "211008",
                    "10.2 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "201071",
                    "10.04 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "245095",
                    "11.94 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wa_all-records_labels.zip", "466566", "24.68 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wa_all-records_labels.zip", "722481", "33.39 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wa_all-records_labels.zip", "402196", "13.8 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wa_all-records_labels.zip", "387805", "23.58 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wa_all-records_labels.zip", "311425", "16.4 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wa_all-records_labels.zip", "485622", "22.64 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wa_all-records_labels.zip", "590758", "25.93 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wa_all-records_labels.zip", "406149", "20.95 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wa_all-records_labels.zip", "473922", "24.62 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wa_all-records_labels.zip", "448753", "23.93 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wa_all-records_labels.zip", "519479", "27.08 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wa_originated-records_labels.zip",
                    "263712",
                    "13.26 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wa_originated-records_labels.zip",
                    "310267",
                    "14.49 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wa_originated-records_labels.zip",
                    "230076",
                    "7.35 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wa_originated-records_labels.zip",
                    "218772",
                    "12.48 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wa_originated-records_labels.zip",
                    "166279",
                    "8.37 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wa_originated-records_labels.zip",
                    "207841",
                    "9.62 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wa_originated-records_labels.zip",
                    "286416",
                    "12.41 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wa_originated-records_labels.zip",
                    "205550",
                    "10.07 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wa_originated-records_labels.zip",
                    "241128",
                    "11.8 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wa_originated-records_labels.zip",
                    "246580",
                    "12.48 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wa_originated-records_labels.zip",
                    "287748",
                    "14.21 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "225231",
                    "7.74 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "215619",
                    "7.08 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "191532",
                    "4.12 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "183367",
                    "7.25 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "133913",
                    "4.63 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "165363",
                    "5.29 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "255387",
                    "7.8 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "174449",
                    "5.8 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "211008",
                    "6.97 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "201071",
                    "6.95 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "245095",
                    "8.25 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wa_all-records_codes.zip", "466566", "16.4 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wa_all-records_codes.zip", "722481", "22.74 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wa_all-records_codes.zip", "402196", "8.75 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wa_all-records_codes.zip", "387805", "15.87 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wa_all-records_codes.zip", "311425", "10.92 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wa_all-records_codes.zip", "485622", "15.32 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wa_all-records_codes.zip", "590758", "17.9 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wa_all-records_codes.zip", "406149", "13.93 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wa_all-records_codes.zip", "473922", "16.26 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wa_all-records_codes.zip", "448753", "15.96 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wa_all-records_codes.zip", "519479", "18.1 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wa_originated-records_codes.zip",
                    "263712",
                    "9.1 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wa_originated-records_codes.zip",
                    "310267",
                    "10.15 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wa_originated-records_codes.zip",
                    "230076",
                    "4.96 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wa_originated-records_codes.zip",
                    "218772",
                    "8.71 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wa_originated-records_codes.zip",
                    "166279",
                    "5.77 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wa_originated-records_codes.zip",
                    "207841",
                    "6.67 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wa_originated-records_codes.zip",
                    "286416",
                    "8.79 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wa_originated-records_codes.zip",
                    "205550",
                    "6.9 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wa_originated-records_codes.zip",
                    "241128",
                    "8.02 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wa_originated-records_codes.zip",
                    "246580",
                    "8.58 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wa_originated-records_codes.zip",
                    "287748",
                    "9.76 MB",
                ),
            },
        },
    },
    "nc": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "220677",
                    "10.93 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "228163",
                    "10.68 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "196986",
                    "6.12 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "190281",
                    "11.14 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "154486",
                    "7.77 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "202793",
                    "9.24 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "263921",
                    "11.18 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "189738",
                    "9.12 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "211447",
                    "10.31 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "224534",
                    "11.35 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "240943",
                    "12.17 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nc_all-records_labels.zip", "519897", "27.86 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nc_all-records_labels.zip", "779619", "36.44 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nc_all-records_labels.zip", "464109", "16.24 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nc_all-records_labels.zip", "457002", "29.06 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nc_all-records_labels.zip", "392549", "21.12 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nc_all-records_labels.zip", "575937", "26.69 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nc_all-records_labels.zip", "617968", "27.09 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nc_all-records_labels.zip", "476288", "24.93 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nc_all-records_labels.zip", "511912", "26.98 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nc_all-records_labels.zip", "562524", "30.51 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nc_all-records_labels.zip", "578793", "31.47 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nc_originated-records_labels.zip",
                    "262765",
                    "13.32 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nc_originated-records_labels.zip",
                    "337640",
                    "15.84 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nc_originated-records_labels.zip",
                    "240128",
                    "7.69 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nc_originated-records_labels.zip",
                    "231114",
                    "13.82 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nc_originated-records_labels.zip",
                    "192473",
                    "9.85 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nc_originated-records_labels.zip",
                    "260693",
                    "12.04 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nc_originated-records_labels.zip",
                    "303410",
                    "13.01 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nc_originated-records_labels.zip",
                    "227079",
                    "11.18 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nc_originated-records_labels.zip",
                    "248590",
                    "12.36 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nc_originated-records_labels.zip",
                    "278062",
                    "14.32 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nc_originated-records_labels.zip",
                    "289407",
                    "14.88 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "220677",
                    "7.49 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "228163",
                    "7.37 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "196986",
                    "4.24 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "190281",
                    "7.64 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "154486",
                    "5.35 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "202793",
                    "6.4 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "263921",
                    "7.94 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "189738",
                    "6.03 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "211447",
                    "6.9 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "224534",
                    "7.74 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "240943",
                    "8.33 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nc_all-records_codes.zip", "519897", "18.52 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nc_all-records_codes.zip", "779619", "24.55 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nc_all-records_codes.zip", "464109", "10.37 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nc_all-records_codes.zip", "457002", "19.13 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nc_all-records_codes.zip", "392549", "13.94 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nc_all-records_codes.zip", "575937", "17.94 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nc_all-records_codes.zip", "617968", "18.62 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nc_all-records_codes.zip", "476288", "15.9 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nc_all-records_codes.zip", "511912", "17.45 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nc_all-records_codes.zip", "562524", "20.11 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nc_all-records_codes.zip", "578793", "20.81 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nc_originated-records_codes.zip",
                    "262765",
                    "9.11 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nc_originated-records_codes.zip",
                    "337640",
                    "10.93 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nc_originated-records_codes.zip",
                    "240128",
                    "5.27 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nc_originated-records_codes.zip",
                    "231114",
                    "9.42 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nc_originated-records_codes.zip",
                    "192473",
                    "6.73 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nc_originated-records_codes.zip",
                    "260693",
                    "8.29 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nc_originated-records_codes.zip",
                    "303410",
                    "9.19 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nc_originated-records_codes.zip",
                    "227079",
                    "7.35 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nc_originated-records_codes.zip",
                    "248590",
                    "8.23 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nc_originated-records_codes.zip",
                    "278062",
                    "9.71 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nc_originated-records_codes.zip",
                    "289407",
                    "10.13 MB",
                ),
            },
        },
    },
    "nd": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15775",
                    "603.58 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "11613",
                    "456.02 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12661",
                    "336.26 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15228",
                    "660.94 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12935",
                    "513.04 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12079",
                    "485.38 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "17245",
                    "600.63 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "14852",
                    "543.35 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "16629",
                    "606.86 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "17550",
                    "663.49 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "19995",
                    "730.61 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nd_all-records_labels.zip", "32670", "1.35 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nd_all-records_labels.zip", "32081", "1.34 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nd_all-records_labels.zip", "25521", "733.11 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nd_all-records_labels.zip", "31382", "1.48 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nd_all-records_labels.zip", "27698", "1.18 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nd_all-records_labels.zip", "28946", "1.25 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nd_all-records_labels.zip", "35789", "1.37 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nd_all-records_labels.zip", "30234", "1.22 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nd_all-records_labels.zip", "32754", "1.34 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nd_all-records_labels.zip", "35576", "1.48 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nd_all-records_labels.zip", "37581", "1.53 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nd_originated-records_labels.zip",
                    "19580",
                    "772.47 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nd_originated-records_labels.zip",
                    "17673",
                    "689.98 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nd_originated-records_labels.zip",
                    "16016",
                    "429.87 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nd_originated-records_labels.zip",
                    "19045",
                    "847.76 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nd_originated-records_labels.zip",
                    "17180",
                    "693.97 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nd_originated-records_labels.zip",
                    "16806",
                    "683.54 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nd_originated-records_labels.zip",
                    "21080",
                    "749.43 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nd_originated-records_labels.zip",
                    "18548",
                    "698.61 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nd_originated-records_labels.zip",
                    "20218",
                    "761.83 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nd_originated-records_labels.zip",
                    "22042",
                    "860.22 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nd_originated-records_labels.zip",
                    "24096",
                    "905.02 KB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15775",
                    "388.61 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "11613",
                    "292.47 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12661",
                    "238.72 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15228",
                    "425.66 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12935",
                    "330.05 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12079",
                    "313.83 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "17245",
                    "399.68 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "14852",
                    "348.81 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "16629",
                    "390.2 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "17550",
                    "426.9 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "19995",
                    "472.27 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nd_all-records_codes.zip", "32670", "832.59 KB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nd_all-records_codes.zip", "32081", "834.25 KB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nd_all-records_codes.zip", "25521", "487.38 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nd_all-records_codes.zip", "31382", "919.39 KB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nd_all-records_codes.zip", "27698", "726.15 KB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nd_all-records_codes.zip", "28946", "781.35 KB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nd_all-records_codes.zip", "35789", "876.82 KB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nd_all-records_codes.zip", "30234", "748.63 KB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nd_all-records_codes.zip", "32754", "826.34 KB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nd_all-records_codes.zip", "35576", "908.14 KB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nd_all-records_codes.zip", "37581", "943.93 KB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nd_originated-records_codes.zip",
                    "19580",
                    "486.75 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nd_originated-records_codes.zip",
                    "17673",
                    "439.38 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nd_originated-records_codes.zip",
                    "16016",
                    "299.25 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nd_originated-records_codes.zip",
                    "19045",
                    "537.29 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nd_originated-records_codes.zip",
                    "17180",
                    "437.05 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nd_originated-records_codes.zip",
                    "16806",
                    "438.4 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nd_originated-records_codes.zip",
                    "21080",
                    "495.22 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nd_originated-records_codes.zip",
                    "18548",
                    "440.47 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nd_originated-records_codes.zip",
                    "20218",
                    "482.84 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nd_originated-records_codes.zip",
                    "22042",
                    "542.74 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nd_originated-records_codes.zip",
                    "24096",
                    "576.32 KB",
                ),
            },
        },
    },
    "ne": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ne_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "42823",
                    "1.96 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ne_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "35882",
                    "1.57 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ne_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "34951",
                    "1.05 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ne_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "38670",
                    "1.94 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ne_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "30830",
                    "1.5 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ne_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "33590",
                    "1.44 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ne_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "56987",
                    "2.26 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ne_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "42269",
                    "1.83 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ne_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "51870",
                    "2.25 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ne_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "45909",
                    "2.1 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ne_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "57432",
                    "2.6 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ne_all-records_labels.zip", "89068", "4.35 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ne_all-records_labels.zip", "112752", "5.1 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ne_all-records_labels.zip", "74966", "2.4 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ne_all-records_labels.zip", "82331", "4.47 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ne_all-records_labels.zip", "68559", "3.58 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ne_all-records_labels.zip", "88586", "3.98 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ne_all-records_labels.zip", "117158", "4.99 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ne_all-records_labels.zip", "90603", "4.29 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ne_all-records_labels.zip", "105043", "4.96 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ne_all-records_labels.zip", "97423", "4.78 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ne_all-records_labels.zip", "113860", "5.56 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ne_originated-records_labels.zip",
                    "52019",
                    "2.41 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ne_originated-records_labels.zip",
                    "51923",
                    "2.26 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ne_originated-records_labels.zip",
                    "43786",
                    "1.32 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ne_originated-records_labels.zip",
                    "48157",
                    "2.46 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ne_originated-records_labels.zip",
                    "39960",
                    "1.98 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ne_originated-records_labels.zip",
                    "44333",
                    "1.92 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ne_originated-records_labels.zip",
                    "65475",
                    "2.65 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ne_originated-records_labels.zip",
                    "50258",
                    "2.23 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ne_originated-records_labels.zip",
                    "59744",
                    "2.64 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ne_originated-records_labels.zip",
                    "56003",
                    "2.6 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ne_originated-records_labels.zip",
                    "67081",
                    "3.09 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ne_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "42823",
                    "1.28 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ne_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "35882",
                    "1.06 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ne_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "34951",
                    "753.37 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ne_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "38670",
                    "1.3 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ne_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "30830",
                    "988.96 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ne_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "33590",
                    "983.97 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ne_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "56987",
                    "1.58 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ne_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "42269",
                    "1.2 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ne_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "51870",
                    "1.48 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ne_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "45909",
                    "1.37 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ne_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "57432",
                    "1.7 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ne_all-records_codes.zip", "89068", "2.76 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ne_all-records_codes.zip", "112752", "3.37 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ne_all-records_codes.zip", "74966", "1.6 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ne_all-records_codes.zip", "82331", "2.91 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ne_all-records_codes.zip", "68559", "2.27 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ne_all-records_codes.zip", "88586", "2.64 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ne_all-records_codes.zip", "117158", "3.39 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ne_all-records_codes.zip", "90603", "2.71 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ne_all-records_codes.zip", "105043", "3.16 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ne_all-records_codes.zip", "97423", "3.04 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ne_all-records_codes.zip", "113860", "3.54 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ne_originated-records_codes.zip",
                    "52019",
                    "1.56 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ne_originated-records_codes.zip",
                    "51923",
                    "1.52 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ne_originated-records_codes.zip",
                    "43786",
                    "932.71 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ne_originated-records_codes.zip",
                    "48157",
                    "1.64 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ne_originated-records_codes.zip",
                    "39960",
                    "1.29 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ne_originated-records_codes.zip",
                    "44333",
                    "1.3 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ne_originated-records_codes.zip",
                    "65475",
                    "1.84 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ne_originated-records_codes.zip",
                    "50258",
                    "1.45 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ne_originated-records_codes.zip",
                    "59744",
                    "1.72 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ne_originated-records_codes.zip",
                    "56003",
                    "1.69 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ne_originated-records_codes.zip",
                    "67081",
                    "2.01 MB",
                ),
            },
        },
    },
    "tn": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "144529",
                    "7.15 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "151937",
                    "7.17 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "133331",
                    "4.11 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "126852",
                    "7.13 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "103024",
                    "5.17 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "123580",
                    "5.68 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "160077",
                    "6.99 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "113228",
                    "5.37 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "128508",
                    "6.09 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "141210",
                    "6.95 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "151750",
                    "7.48 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tn_all-records_labels.zip", "350490", "18.5 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tn_all-records_labels.zip", "512117", "24.54 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tn_all-records_labels.zip", "326416", "11.11 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tn_all-records_labels.zip", "305114", "18.47 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tn_all-records_labels.zip", "265214", "14.16 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tn_all-records_labels.zip", "365839", "17.39 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tn_all-records_labels.zip", "406028", "18.65 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tn_all-records_labels.zip", "304377", "16.01 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tn_all-records_labels.zip", "335917", "17.65 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tn_all-records_labels.zip", "358454", "19.31 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tn_all-records_labels.zip", "373362", "20.16 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tn_originated-records_labels.zip",
                    "174965",
                    "8.84 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tn_originated-records_labels.zip",
                    "217392",
                    "10.46 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tn_originated-records_labels.zip",
                    "164577",
                    "5.23 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tn_originated-records_labels.zip",
                    "155616",
                    "8.89 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tn_originated-records_labels.zip",
                    "131171",
                    "6.76 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tn_originated-records_labels.zip",
                    "163188",
                    "7.73 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tn_originated-records_labels.zip",
                    "187776",
                    "8.43 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tn_originated-records_labels.zip",
                    "137943",
                    "6.74 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tn_originated-records_labels.zip",
                    "153282",
                    "7.46 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tn_originated-records_labels.zip",
                    "172612",
                    "8.61 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tn_originated-records_labels.zip",
                    "180686",
                    "9.04 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "144529",
                    "4.86 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "151937",
                    "4.92 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "133331",
                    "2.88 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "126852",
                    "4.92 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "103024",
                    "3.53 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "123580",
                    "3.92 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "160077",
                    "4.89 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "113228",
                    "3.56 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "128508",
                    "4.04 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "141210",
                    "4.68 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "151750",
                    "5.03 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tn_all-records_codes.zip", "350490", "12.18 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tn_all-records_codes.zip", "512117", "16.43 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tn_all-records_codes.zip", "326416", "7.18 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tn_all-records_codes.zip", "305114", "12.28 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tn_all-records_codes.zip", "265214", "9.33 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tn_all-records_codes.zip", "365839", "11.7 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tn_all-records_codes.zip", "406028", "12.76 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tn_all-records_codes.zip", "304377", "10.33 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tn_all-records_codes.zip", "335917", "11.45 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tn_all-records_codes.zip", "358454", "12.68 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tn_all-records_codes.zip", "373362", "13.3 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_tn_originated-records_codes.zip",
                    "174965",
                    "6 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_tn_originated-records_codes.zip",
                    "217392",
                    "7.22 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_tn_originated-records_codes.zip",
                    "164577",
                    "3.62 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_tn_originated-records_codes.zip",
                    "155616",
                    "6.1 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_tn_originated-records_codes.zip",
                    "131171",
                    "4.61 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_tn_originated-records_codes.zip",
                    "163188",
                    "5.35 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_tn_originated-records_codes.zip",
                    "187776",
                    "5.9 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_tn_originated-records_codes.zip",
                    "137943",
                    "4.45 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_tn_originated-records_codes.zip",
                    "153282",
                    "4.93 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_tn_originated-records_codes.zip",
                    "172612",
                    "5.75 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_tn_originated-records_codes.zip",
                    "180686",
                    "6.04 MB",
                ),
            },
        },
    },
    "ny": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ny_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "199204",
                    "10.43 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ny_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "281690",
                    "14.06 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ny_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "187337",
                    "6.57 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ny_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "182621",
                    "10.44 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ny_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "156647",
                    "8.24 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ny_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "195917",
                    "9.68 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ny_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "245556",
                    "11.46 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ny_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "201157",
                    "10.32 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ny_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "217296",
                    "11.01 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ny_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "225700",
                    "11.8 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ny_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "242701",
                    "12.39 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ny_all-records_labels.zip", "477313", "26.86 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ny_all-records_labels.zip",
                    "1009451",
                    "51.35 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ny_all-records_labels.zip", "446902", "17.47 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ny_all-records_labels.zip", "439654", "27.13 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ny_all-records_labels.zip", "389279", "22.13 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ny_all-records_labels.zip", "644647", "33.21 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ny_all-records_labels.zip", "645487", "31.84 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ny_all-records_labels.zip", "503733", "28.17 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ny_all-records_labels.zip", "529869", "29.46 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ny_all-records_labels.zip", "539217", "30.46 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ny_all-records_labels.zip", "566980", "31.53 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ny_originated-records_labels.zip",
                    "246292",
                    "13.15 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ny_originated-records_labels.zip",
                    "398639",
                    "20.13 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ny_originated-records_labels.zip",
                    "236499",
                    "8.45 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ny_originated-records_labels.zip",
                    "228054",
                    "13.23 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ny_originated-records_labels.zip",
                    "198817",
                    "10.63 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ny_originated-records_labels.zip",
                    "252826",
                    "12.72 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ny_originated-records_labels.zip",
                    "281652",
                    "13.38 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ny_originated-records_labels.zip",
                    "238554",
                    "12.42 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ny_originated-records_labels.zip",
                    "252729",
                    "13.07 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ny_originated-records_labels.zip",
                    "271829",
                    "14.42 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ny_originated-records_labels.zip",
                    "285106",
                    "14.71 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ny_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "199204",
                    "7.47 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ny_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "281690",
                    "10.14 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ny_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "187337",
                    "4.66 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ny_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "182621",
                    "7.46 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ny_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "156647",
                    "5.87 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ny_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "195917",
                    "6.98 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ny_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "245556",
                    "8.36 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ny_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "201157",
                    "7.36 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ny_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "217296",
                    "7.85 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ny_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "225700",
                    "8.44 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ny_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "242701",
                    "8.82 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ny_all-records_codes.zip", "477313", "18.61 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ny_all-records_codes.zip", "1009451", "35.76 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ny_all-records_codes.zip", "446902", "11.54 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ny_all-records_codes.zip", "439654", "18.57 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ny_all-records_codes.zip", "389279", "15.25 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ny_all-records_codes.zip", "644647", "23.18 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ny_all-records_codes.zip", "645487", "22.45 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ny_all-records_codes.zip", "503733", "19.55 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ny_all-records_codes.zip", "529869", "20.47 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ny_all-records_codes.zip", "539217", "21.23 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ny_all-records_codes.zip", "566980", "21.92 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ny_originated-records_codes.zip",
                    "246292",
                    "9.34 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ny_originated-records_codes.zip",
                    "398639",
                    "14.43 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ny_originated-records_codes.zip",
                    "236499",
                    "5.9 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ny_originated-records_codes.zip",
                    "228054",
                    "9.33 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ny_originated-records_codes.zip",
                    "198817",
                    "7.49 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ny_originated-records_codes.zip",
                    "252826",
                    "9.14 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ny_originated-records_codes.zip",
                    "281652",
                    "9.73 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ny_originated-records_codes.zip",
                    "238554",
                    "8.78 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ny_originated-records_codes.zip",
                    "252729",
                    "9.27 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ny_originated-records_codes.zip",
                    "271829",
                    "10.23 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ny_originated-records_codes.zip",
                    "285106",
                    "10.38 MB",
                ),
            },
        },
    },
    "pa": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "226492",
                    "11.67 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "276621",
                    "13.86 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "200046",
                    "6.74 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "206884",
                    "12.08 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "175312",
                    "8.94 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "230119",
                    "11.38 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "318871",
                    "14.7 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "247649",
                    "12.37 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "280178",
                    "14.07 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "269808",
                    "13.79 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pa_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "313974",
                    "15.99 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pa_all-records_labels.zip", "526005", "29.04 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pa_all-records_labels.zip", "992904", "49.57 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pa_all-records_labels.zip", "473757", "17.91 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pa_all-records_labels.zip", "481331", "30.25 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pa_all-records_labels.zip", "427665", "23.41 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pa_all-records_labels.zip", "713995", "35.8 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pa_all-records_labels.zip", "768245", "37 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pa_all-records_labels.zip", "593240", "32.54 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pa_all-records_labels.zip", "659124", "36.22 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pa_all-records_labels.zip", "619770", "34.49 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pa_all-records_labels.zip", "695500", "38.56 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pa_originated-records_labels.zip",
                    "273334",
                    "14.35 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pa_originated-records_labels.zip",
                    "427955",
                    "21.49 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pa_originated-records_labels.zip",
                    "249620",
                    "8.62 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pa_originated-records_labels.zip",
                    "254361",
                    "15.02 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pa_originated-records_labels.zip",
                    "222765",
                    "11.62 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pa_originated-records_labels.zip",
                    "322031",
                    "16.08 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pa_originated-records_labels.zip",
                    "374957",
                    "17.61 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pa_originated-records_labels.zip",
                    "297874",
                    "15.19 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pa_originated-records_labels.zip",
                    "334150",
                    "17.16 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pa_originated-records_labels.zip",
                    "328425",
                    "16.99 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pa_originated-records_labels.zip",
                    "369571",
                    "19.04 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "226492",
                    "8.16 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "276621",
                    "9.82 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "200046",
                    "4.79 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "206884",
                    "8.4 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "175312",
                    "6.24 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "230119",
                    "8.1 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "318871",
                    "10.64 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "247649",
                    "8.65 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "280178",
                    "9.85 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "269808",
                    "9.72 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pa_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "313974",
                    "11.2 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pa_all-records_codes.zip", "526005", "19.65 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pa_all-records_codes.zip", "992904", "34.13 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pa_all-records_codes.zip", "473757", "11.77 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pa_all-records_codes.zip", "481331", "20.19 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pa_all-records_codes.zip", "427665", "15.79 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pa_all-records_codes.zip", "713995", "24.78 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pa_all-records_codes.zip", "768245", "25.9 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pa_all-records_codes.zip", "593240", "22.19 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pa_all-records_codes.zip", "659124", "24.67 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pa_all-records_codes.zip", "619770", "23.66 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pa_all-records_codes.zip", "695500", "26.36 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pa_originated-records_codes.zip",
                    "273334",
                    "9.99 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pa_originated-records_codes.zip",
                    "427955",
                    "15.19 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pa_originated-records_codes.zip",
                    "249620",
                    "6.04 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pa_originated-records_codes.zip",
                    "254361",
                    "10.34 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pa_originated-records_codes.zip",
                    "222765",
                    "8.07 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pa_originated-records_codes.zip",
                    "322031",
                    "11.45 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pa_originated-records_codes.zip",
                    "374957",
                    "12.74 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pa_originated-records_codes.zip",
                    "297874",
                    "10.53 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pa_originated-records_codes.zip",
                    "334150",
                    "11.94 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pa_originated-records_codes.zip",
                    "328425",
                    "11.84 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pa_originated-records_codes.zip",
                    "369571",
                    "13.21 MB",
                ),
            },
        },
    },
    "ca": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ca_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "1007181",
                    "54.33 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ca_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "870274",
                    "44.14 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ca_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "721751",
                    "25.58 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ca_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "840549",
                    "50.22 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ca_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "617503",
                    "32.89 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ca_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "540095",
                    "26.82 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ca_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "871218",
                    "40.28 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ca_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "777800",
                    "41.39 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ca_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "867778",
                    "45.96 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ca_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "943566",
                    "51.22 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ca_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "1179705",
                    "63.7 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ca_all-records_labels.zip",
                    "2235971",
                    "128.67 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ca_all-records_labels.zip",
                    "3425570",
                    "178.89 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ca_all-records_labels.zip",
                    "1714459",
                    "68.82 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ca_all-records_labels.zip",
                    "1878495",
                    "120.02 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ca_all-records_labels.zip",
                    "1436457",
                    "81.73 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ca_all-records_labels.zip",
                    "1843875",
                    "91.09 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ca_all-records_labels.zip",
                    "2186032",
                    "102.95 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ca_all-records_labels.zip",
                    "1914815",
                    "108.47 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ca_all-records_labels.zip",
                    "2007593",
                    "113.6 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ca_all-records_labels.zip",
                    "2161214",
                    "124.84 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ca_all-records_labels.zip",
                    "2541978",
                    "146.32 MB",
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ca_originated-records_labels.zip",
                    "1172541",
                    "63.86 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ca_originated-records_labels.zip",
                    "1233502",
                    "62.47 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ca_originated-records_labels.zip",
                    "877753",
                    "31.88 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ca_originated-records_labels.zip",
                    "993335",
                    "60.03 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ca_originated-records_labels.zip",
                    "750422",
                    "40.44 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ca_originated-records_labels.zip",
                    "672822",
                    "33.65 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ca_originated-records_labels.zip",
                    "972974",
                    "45.3 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ca_originated-records_labels.zip",
                    "917070",
                    "49.28 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ca_originated-records_labels.zip",
                    "980348",
                    "52.43 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ca_originated-records_labels.zip",
                    "1153965",
                    "63.32 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ca_originated-records_labels.zip",
                    "1391720",
                    "75.92 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ca_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "1007181",
                    "40 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ca_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "870274",
                    "32.16 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ca_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "721751",
                    "17.18 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ca_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "840549",
                    "35.92 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ca_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "617503",
                    "24.08 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ca_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "540095",
                    "19.47 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ca_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "871218",
                    "29.59 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ca_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "777800",
                    "30.2 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ca_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "867778",
                    "33.54 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ca_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "943566",
                    "37.62 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ca_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "1179705",
                    "46.88 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ca_all-records_codes.zip", "2235971", "91.67 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ca_all-records_codes.zip",
                    "3425570",
                    "117.94 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ca_all-records_codes.zip", "1714459", "42.19 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ca_all-records_codes.zip", "1878495", "82.3 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ca_all-records_codes.zip", "1436457", "57.96 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ca_all-records_codes.zip", "1843875", "63.68 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ca_all-records_codes.zip", "2186032", "72.66 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ca_all-records_codes.zip", "1914815", "76.92 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ca_all-records_codes.zip", "2007593", "80.32 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ca_all-records_codes.zip", "2161214", "88.6 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ca_all-records_codes.zip", "2541978", "104.3 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ca_originated-records_codes.zip",
                    "1172541",
                    "46.78 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ca_originated-records_codes.zip",
                    "1233502",
                    "45.28 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ca_originated-records_codes.zip",
                    "877753",
                    "21.13 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ca_originated-records_codes.zip",
                    "993335",
                    "42.66 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ca_originated-records_codes.zip",
                    "750422",
                    "29.45 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ca_originated-records_codes.zip",
                    "672822",
                    "24.32 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ca_originated-records_codes.zip",
                    "972974",
                    "33.15 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ca_originated-records_codes.zip",
                    "917070",
                    "35.8 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ca_originated-records_codes.zip",
                    "980348",
                    "38.11 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ca_originated-records_codes.zip",
                    "1153965",
                    "46.26 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ca_originated-records_codes.zip",
                    "1391720",
                    "55.58 MB",
                ),
            },
        },
    },
    "nv": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "84481",
                    "3.96 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "73747",
                    "3.21 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "76783",
                    "2.28 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "69214",
                    "3.49 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "49799",
                    "2.4 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "48287",
                    "1.93 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "59437",
                    "2.29 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "39765",
                    "1.65 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "47126",
                    "2.01 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "62574",
                    "2.95 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "67783",
                    "3.09 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nv_all-records_labels.zip", "196764", "9.88 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nv_all-records_labels.zip", "326985", "14.53 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nv_all-records_labels.zip", "178587", "5.91 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nv_all-records_labels.zip", "158259", "8.69 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nv_all-records_labels.zip", "119744", "6.27 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nv_all-records_labels.zip", "163606", "6.93 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nv_all-records_labels.zip", "168658", "6.88 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nv_all-records_labels.zip", "112858", "5.27 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nv_all-records_labels.zip", "126313", "5.98 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nv_all-records_labels.zip", "151453", "7.8 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nv_all-records_labels.zip", "161343", "8.12 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nv_originated-records_labels.zip",
                    "97926",
                    "4.69 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nv_originated-records_labels.zip",
                    "113248",
                    "5 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nv_originated-records_labels.zip",
                    "91540",
                    "2.8 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nv_originated-records_labels.zip",
                    "81624",
                    "4.21 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nv_originated-records_labels.zip",
                    "61757",
                    "3.04 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nv_originated-records_labels.zip",
                    "62592",
                    "2.58 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nv_originated-records_labels.zip",
                    "70049",
                    "2.77 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nv_originated-records_labels.zip",
                    "51445",
                    "2.24 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nv_originated-records_labels.zip",
                    "57173",
                    "2.51 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nv_originated-records_labels.zip",
                    "82011",
                    "3.96 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nv_originated-records_labels.zip",
                    "86528",
                    "4.04 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "84481",
                    "2.78 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "73747",
                    "2.26 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "76783",
                    "1.59 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "69214",
                    "2.48 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "49799",
                    "1.68 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "48287",
                    "1.36 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "59437",
                    "1.63 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "39765",
                    "1.13 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "47126",
                    "1.37 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "62574",
                    "2.07 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "67783",
                    "2.17 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nv_all-records_codes.zip", "196764", "6.71 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nv_all-records_codes.zip", "326985", "9.91 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nv_all-records_codes.zip", "178587", "3.8 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nv_all-records_codes.zip", "158259", "5.91 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nv_all-records_codes.zip", "119744", "4.26 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nv_all-records_codes.zip", "163606", "4.74 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nv_all-records_codes.zip", "168658", "4.74 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nv_all-records_codes.zip", "112858", "3.48 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nv_all-records_codes.zip", "126313", "3.93 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nv_all-records_codes.zip", "151453", "5.33 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nv_all-records_codes.zip", "161343", "5.54 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_nv_originated-records_codes.zip",
                    "97926",
                    "3.28 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_nv_originated-records_codes.zip",
                    "113248",
                    "3.54 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_nv_originated-records_codes.zip",
                    "91540",
                    "1.93 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_nv_originated-records_codes.zip",
                    "81624",
                    "2.98 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_nv_originated-records_codes.zip",
                    "61757",
                    "2.13 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_nv_originated-records_codes.zip",
                    "62592",
                    "1.82 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_nv_originated-records_codes.zip",
                    "70049",
                    "1.98 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_nv_originated-records_codes.zip",
                    "51445",
                    "1.52 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_nv_originated-records_codes.zip",
                    "57173",
                    "1.7 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_nv_originated-records_codes.zip",
                    "82011",
                    "2.79 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_nv_originated-records_codes.zip",
                    "86528",
                    "2.82 MB",
                ),
            },
        },
    },
    "pr": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pr_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "16754",
                    "783.1 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pr_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "35822",
                    "1.56 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pr_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12257",
                    "361.87 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pr_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "18782",
                    "893.63 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pr_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "20640",
                    "942.76 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pr_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "36283",
                    "1.5 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pr_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "34669",
                    "1.37 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pr_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "25832",
                    "1.11 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pr_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "25342",
                    "1.08 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pr_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "30144",
                    "1.35 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pr_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "31083",
                    "1.38 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pr_all-records_labels.zip", "55699", "2.78 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pr_all-records_labels.zip", "141905", "6.23 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pr_all-records_labels.zip", "41775", "1.3 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pr_all-records_labels.zip", "58798", "2.92 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pr_all-records_labels.zip", "69716", "3.45 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pr_all-records_labels.zip", "121121", "5.16 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pr_all-records_labels.zip", "117907", "4.79 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pr_all-records_labels.zip", "85316", "3.93 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pr_all-records_labels.zip", "83046", "3.88 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pr_all-records_labels.zip", "96530", "4.63 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pr_all-records_labels.zip", "87162", "4.17 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pr_originated-records_labels.zip",
                    "26124",
                    "1.23 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pr_originated-records_labels.zip",
                    "57036",
                    "2.51 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pr_originated-records_labels.zip",
                    "19395",
                    "576.04 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pr_originated-records_labels.zip",
                    "28616",
                    "1.37 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pr_originated-records_labels.zip",
                    "30528",
                    "1.42 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pr_originated-records_labels.zip",
                    "50632",
                    "2.14 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pr_originated-records_labels.zip",
                    "46237",
                    "1.86 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pr_originated-records_labels.zip",
                    "37660",
                    "1.66 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pr_originated-records_labels.zip",
                    "35121",
                    "1.55 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pr_originated-records_labels.zip",
                    "40075",
                    "1.8 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pr_originated-records_labels.zip",
                    "40616",
                    "1.81 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pr_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "16754",
                    "536.87 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pr_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "35822",
                    "1.08 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pr_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12257",
                    "255.16 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pr_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "18782",
                    "614.78 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pr_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "20640",
                    "647.5 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pr_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "36283",
                    "1.05 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pr_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "34669",
                    "973.6 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pr_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "25832",
                    "756.02 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pr_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "25342",
                    "737.14 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pr_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "30144",
                    "925.82 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pr_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "31083",
                    "942.8 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pr_all-records_codes.zip", "55699", "1.82 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pr_all-records_codes.zip", "141905", "4.18 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pr_all-records_codes.zip", "41775", "873.01 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pr_all-records_codes.zip", "58798", "1.94 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pr_all-records_codes.zip", "69716", "2.27 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pr_all-records_codes.zip", "121121", "3.48 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pr_all-records_codes.zip", "117907", "3.28 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pr_all-records_codes.zip", "85316", "2.56 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pr_all-records_codes.zip", "83046", "2.54 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pr_all-records_codes.zip", "96530", "3.04 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pr_all-records_codes.zip", "87162", "2.75 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_pr_originated-records_codes.zip",
                    "26124",
                    "835.09 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_pr_originated-records_codes.zip",
                    "57036",
                    "1.73 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_pr_originated-records_codes.zip",
                    "19395",
                    "406.77 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_pr_originated-records_codes.zip",
                    "28616",
                    "942.61 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_pr_originated-records_codes.zip",
                    "30528",
                    "963.45 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_pr_originated-records_codes.zip",
                    "50632",
                    "1.49 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_pr_originated-records_codes.zip",
                    "46237",
                    "1.32 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_pr_originated-records_codes.zip",
                    "37660",
                    "1.13 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_pr_originated-records_codes.zip",
                    "35121",
                    "1.05 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_pr_originated-records_codes.zip",
                    "40075",
                    "1.23 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_pr_originated-records_codes.zip",
                    "40616",
                    "1.24 MB",
                ),
            },
        },
    },
    "de": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_de_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "21457",
                    "907.27 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_de_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "24785",
                    "1.05 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_de_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "18891",
                    "540.64 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_de_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "18365",
                    "848.09 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_de_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "14206",
                    "642.68 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_de_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "19350",
                    "807.78 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_de_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "26431",
                    "1.05 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_de_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "18557",
                    "764.88 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_de_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "21244",
                    "862.31 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_de_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "22603",
                    "952.26 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_de_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "25372",
                    "1.06 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_de_all-records_labels.zip", "56002", "2.64 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_de_all-records_labels.zip", "102001", "4.48 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_de_all-records_labels.zip", "49695", "1.64 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_de_all-records_labels.zip", "48176", "2.44 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_de_all-records_labels.zip", "39784", "2 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_de_all-records_labels.zip", "68856", "3.06 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_de_all-records_labels.zip", "72398", "3.14 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_de_all-records_labels.zip", "52039", "2.43 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_de_all-records_labels.zip", "57559", "2.66 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_de_all-records_labels.zip", "59314", "2.83 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_de_all-records_labels.zip", "65069", "3.06 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_de_originated-records_labels.zip",
                    "27296",
                    "1.18 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_de_originated-records_labels.zip",
                    "40053",
                    "1.69 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_de_originated-records_labels.zip",
                    "24719",
                    "718.05 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_de_originated-records_labels.zip",
                    "24062",
                    "1.14 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_de_originated-records_labels.zip",
                    "19181",
                    "882.64 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_de_originated-records_labels.zip",
                    "27619",
                    "1.17 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_de_originated-records_labels.zip",
                    "32995",
                    "1.31 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_de_originated-records_labels.zip",
                    "24377",
                    "1.01 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_de_originated-records_labels.zip",
                    "26997",
                    "1.1 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_de_originated-records_labels.zip",
                    "30167",
                    "1.28 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_de_originated-records_labels.zip",
                    "32868",
                    "1.38 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_de_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "21457",
                    "600.87 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_de_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "24785",
                    "699.02 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_de_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "18891",
                    "376.86 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_de_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "18365",
                    "563.01 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_de_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "14206",
                    "424.11 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_de_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "19350",
                    "544.41 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_de_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "26431",
                    "709.46 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_de_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "18557",
                    "497.81 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_de_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "21244",
                    "559.01 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_de_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "22603",
                    "621.51 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_de_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "25372",
                    "689 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_de_all-records_codes.zip", "56002", "1.68 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_de_all-records_codes.zip", "102001", "2.91 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_de_all-records_codes.zip", "49695", "1.09 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_de_all-records_codes.zip", "48176", "1.54 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_de_all-records_codes.zip", "39784", "1.26 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_de_all-records_codes.zip", "68856", "2 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_de_all-records_codes.zip", "72398", "2.07 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_de_all-records_codes.zip", "52039", "1.52 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_de_all-records_codes.zip", "57559", "1.66 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_de_all-records_codes.zip", "59314", "1.77 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_de_all-records_codes.zip", "65069", "1.92 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_de_originated-records_codes.zip",
                    "27296",
                    "769.27 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_de_originated-records_codes.zip",
                    "40053",
                    "1.12 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_de_originated-records_codes.zip",
                    "24719",
                    "494.64 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_de_originated-records_codes.zip",
                    "24062",
                    "748.52 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_de_originated-records_codes.zip",
                    "19181",
                    "575.97 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_de_originated-records_codes.zip",
                    "27619",
                    "775.49 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_de_originated-records_codes.zip",
                    "32995",
                    "882.98 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_de_originated-records_codes.zip",
                    "24377",
                    "652.39 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_de_originated-records_codes.zip",
                    "26997",
                    "709.17 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_de_originated-records_codes.zip",
                    "30167",
                    "829.22 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_de_originated-records_codes.zip",
                    "32868",
                    "897.42 KB",
                ),
            },
        },
    },
    "dc": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_dc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15924",
                    "720.67 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_dc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "16676",
                    "696.13 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_dc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12419",
                    "384.38 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_dc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "14290",
                    "659.64 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_dc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "11399",
                    "518.92 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_dc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12148",
                    "506.83 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_dc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "18262",
                    "731.02 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_dc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15280",
                    "677.01 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_dc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "16225",
                    "712.21 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_dc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "17499",
                    "785.67 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_dc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "20716",
                    "908.46 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_dc_all-records_labels.zip", "38399", "1.87 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_dc_all-records_labels.zip", "53480", "2.43 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_dc_all-records_labels.zip", "30927", "1.07 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_dc_all-records_labels.zip", "34958", "1.77 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_dc_all-records_labels.zip", "28672", "1.42 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_dc_all-records_labels.zip", "33505", "1.55 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_dc_all-records_labels.zip", "43540", "1.9 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_dc_all-records_labels.zip", "37657", "1.81 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_dc_all-records_labels.zip", "38173", "1.84 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_dc_all-records_labels.zip", "43020", "2.11 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_dc_all-records_labels.zip", "48621", "2.34 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_dc_originated-records_labels.zip",
                    "19324",
                    "891.94 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_dc_originated-records_labels.zip",
                    "23948",
                    "998.05 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_dc_originated-records_labels.zip",
                    "15414",
                    "483 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_dc_originated-records_labels.zip",
                    "17821",
                    "839.5 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_dc_originated-records_labels.zip",
                    "14547",
                    "676.21 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_dc_originated-records_labels.zip",
                    "15212",
                    "643.03 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_dc_originated-records_labels.zip",
                    "20287",
                    "823.05 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_dc_originated-records_labels.zip",
                    "18123",
                    "817.1 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_dc_originated-records_labels.zip",
                    "18511",
                    "828.68 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_dc_originated-records_labels.zip",
                    "21877",
                    "1 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_dc_originated-records_labels.zip",
                    "24842",
                    "1.12 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_dc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15924",
                    "457.4 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_dc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "16676",
                    "454.07 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_dc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12419",
                    "259.55 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_dc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "14290",
                    "415.87 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_dc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "11399",
                    "327.64 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_dc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12148",
                    "331.88 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_dc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "18262",
                    "485.74 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_dc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15280",
                    "423.44 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_dc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "16225",
                    "446.48 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_dc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "17499",
                    "493.75 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_dc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "20716",
                    "567.98 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_dc_all-records_codes.zip", "38399", "1.15 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_dc_all-records_codes.zip", "53480", "1.55 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_dc_all-records_codes.zip", "30927", "685.42 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_dc_all-records_codes.zip", "34958", "1.07 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_dc_all-records_codes.zip", "28672", "862.7 KB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_dc_all-records_codes.zip", "33505", "982.73 KB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_dc_all-records_codes.zip", "43540", "1.21 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_dc_all-records_codes.zip", "37657", "1.1 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_dc_all-records_codes.zip", "38173", "1.11 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_dc_all-records_codes.zip", "43020", "1.28 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_dc_all-records_codes.zip", "48621", "1.42 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_dc_originated-records_codes.zip",
                    "19324",
                    "561.87 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_dc_originated-records_codes.zip",
                    "23948",
                    "647.59 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_dc_originated-records_codes.zip",
                    "15414",
                    "321.38 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_dc_originated-records_codes.zip",
                    "17821",
                    "524.36 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_dc_originated-records_codes.zip",
                    "14547",
                    "423.92 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_dc_originated-records_codes.zip",
                    "15212",
                    "416.59 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_dc_originated-records_codes.zip",
                    "20287",
                    "542.45 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_dc_originated-records_codes.zip",
                    "18123",
                    "507.21 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_dc_originated-records_codes.zip",
                    "18511",
                    "514.35 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_dc_originated-records_codes.zip",
                    "21877",
                    "626.77 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_dc_originated-records_codes.zip",
                    "24842",
                    "691.5 KB",
                ),
            },
        },
    },
    "wi": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "141247",
                    "6.63 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "140939",
                    "6.7 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "118149",
                    "3.66 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "126112",
                    "6.94 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "99338",
                    "5.08 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "140787",
                    "6.42 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "233978",
                    "9.45 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "159084",
                    "7.03 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "197382",
                    "8.86 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "155945",
                    "7.35 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "219594",
                    "10.08 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wi_all-records_labels.zip", "277224", "14.04 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wi_all-records_labels.zip", "460622", "22.04 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wi_all-records_labels.zip", "237542", "8.25 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wi_all-records_labels.zip", "250077", "14.91 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wi_all-records_labels.zip", "207239", "11.5 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wi_all-records_labels.zip", "359119", "16.92 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wi_all-records_labels.zip", "475760", "20.37 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wi_all-records_labels.zip", "324321", "15.85 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wi_all-records_labels.zip", "394638", "19.35 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wi_all-records_labels.zip", "306118", "15.66 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wi_all-records_labels.zip", "398029", "19.93 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wi_originated-records_labels.zip",
                    "168678",
                    "8.06 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wi_originated-records_labels.zip",
                    "211916",
                    "10.01 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wi_originated-records_labels.zip",
                    "146251",
                    "4.59 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wi_originated-records_labels.zip",
                    "153515",
                    "8.58 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wi_originated-records_labels.zip",
                    "124916",
                    "6.51 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wi_originated-records_labels.zip",
                    "187234",
                    "8.58 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wi_originated-records_labels.zip",
                    "270190",
                    "11.1 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wi_originated-records_labels.zip",
                    "188288",
                    "8.56 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wi_originated-records_labels.zip",
                    "228537",
                    "10.45 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wi_originated-records_labels.zip",
                    "188524",
                    "9.07 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wi_originated-records_labels.zip",
                    "253728",
                    "11.88 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "141247",
                    "4.45 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "140939",
                    "4.6 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "118149",
                    "2.59 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "126112",
                    "4.69 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "99338",
                    "3.39 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "140787",
                    "4.45 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "233978",
                    "6.72 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "159084",
                    "4.64 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "197382",
                    "5.93 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "155945",
                    "4.93 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "219594",
                    "6.71 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wi_all-records_codes.zip", "277224", "9.08 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wi_all-records_codes.zip", "460622", "14.82 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wi_all-records_codes.zip", "237542", "5.41 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wi_all-records_codes.zip", "250077", "9.7 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wi_all-records_codes.zip", "207239", "7.39 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wi_all-records_codes.zip", "359119", "11.47 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wi_all-records_codes.zip", "475760", "14.08 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wi_all-records_codes.zip", "324321", "10.14 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wi_all-records_codes.zip", "394638", "12.55 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wi_all-records_codes.zip", "306118", "10.17 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wi_all-records_codes.zip", "398029", "12.88 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wi_originated-records_codes.zip",
                    "168678",
                    "5.37 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wi_originated-records_codes.zip",
                    "211916",
                    "6.85 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wi_originated-records_codes.zip",
                    "146251",
                    "3.19 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wi_originated-records_codes.zip",
                    "153515",
                    "5.74 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wi_originated-records_codes.zip",
                    "124916",
                    "4.3 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wi_originated-records_codes.zip",
                    "187234",
                    "5.9 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wi_originated-records_codes.zip",
                    "270190",
                    "7.86 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wi_originated-records_codes.zip",
                    "188288",
                    "5.6 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wi_originated-records_codes.zip",
                    "228537",
                    "6.95 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wi_originated-records_codes.zip",
                    "188524",
                    "6.03 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wi_originated-records_codes.zip",
                    "253728",
                    "7.85 MB",
                ),
            },
        },
    },
    "wv": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "23752",
                    "1.15 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "32932",
                    "1.43 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "22635",
                    "775.09 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "22216",
                    "1.16 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "20952",
                    "925.27 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "27892",
                    "1.25 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "31766",
                    "1.38 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "25662",
                    "1.09 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "26690",
                    "1.13 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "29841",
                    "1.37 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wv_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "30400",
                    "1.36 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wv_all-records_labels.zip", "59932", "3.14 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wv_all-records_labels.zip", "108639", "4.82 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wv_all-records_labels.zip", "56407", "2.02 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wv_all-records_labels.zip", "56189", "3.18 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wv_all-records_labels.zip", "53804", "2.59 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wv_all-records_labels.zip", "82256", "3.81 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wv_all-records_labels.zip", "78726", "3.62 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wv_all-records_labels.zip", "65054", "3.02 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wv_all-records_labels.zip", "67127", "3.14 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wv_all-records_labels.zip", "71730", "3.58 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wv_all-records_labels.zip", "71668", "3.48 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wv_originated-records_labels.zip",
                    "31084",
                    "1.54 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wv_originated-records_labels.zip",
                    "49942",
                    "2.16 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wv_originated-records_labels.zip",
                    "29490",
                    "1.02 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wv_originated-records_labels.zip",
                    "29892",
                    "1.59 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wv_originated-records_labels.zip",
                    "28288",
                    "1.28 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wv_originated-records_labels.zip",
                    "39173",
                    "1.77 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wv_originated-records_labels.zip",
                    "40090",
                    "1.78 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wv_originated-records_labels.zip",
                    "33089",
                    "1.44 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wv_originated-records_labels.zip",
                    "34262",
                    "1.49 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wv_originated-records_labels.zip",
                    "38630",
                    "1.82 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wv_originated-records_labels.zip",
                    "38585",
                    "1.77 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "23752",
                    "731.44 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "32932",
                    "927.05 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "22635",
                    "535.47 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "22216",
                    "750.99 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "20952",
                    "586.49 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "27892",
                    "805.27 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "31766",
                    "906.21 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "25662",
                    "682.61 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "26690",
                    "718.48 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "29841",
                    "869.85 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wv_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "30400",
                    "859.14 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wv_all-records_codes.zip", "59932", "1.9 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wv_all-records_codes.zip", "108639", "3.05 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wv_all-records_codes.zip", "56407", "1.32 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wv_all-records_codes.zip", "56189", "1.97 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wv_all-records_codes.zip", "53804", "1.57 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wv_all-records_codes.zip", "82256", "2.4 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wv_all-records_codes.zip", "78726", "2.31 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wv_all-records_codes.zip", "65054", "1.83 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wv_all-records_codes.zip", "67127", "1.91 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wv_all-records_codes.zip", "71730", "2.18 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wv_all-records_codes.zip", "71668", "2.12 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wv_originated-records_codes.zip",
                    "31084",
                    "966.37 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wv_originated-records_codes.zip",
                    "49942",
                    "1.39 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wv_originated-records_codes.zip",
                    "29490",
                    "694.72 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wv_originated-records_codes.zip",
                    "29892",
                    "1.02 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wv_originated-records_codes.zip",
                    "28288",
                    "806.54 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wv_originated-records_codes.zip",
                    "39173",
                    "1.14 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wv_originated-records_codes.zip",
                    "40090",
                    "1.16 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wv_originated-records_codes.zip",
                    "33089",
                    "896.24 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wv_originated-records_codes.zip",
                    "34262",
                    "933.86 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wv_originated-records_codes.zip",
                    "38630",
                    "1.14 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wv_originated-records_codes.zip",
                    "38585",
                    "1.11 MB",
                ),
            },
        },
    },
    "hi": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_hi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "25790",
                    "1.11 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_hi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "26443",
                    "1.11 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_hi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "20146",
                    "641.16 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_hi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "21679",
                    "993.8 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_hi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "16100",
                    "691.11 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_hi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "19577",
                    "808.1 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_hi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "31476",
                    "1.18 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_hi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "22003",
                    "927.28 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_hi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "24636",
                    "1.02 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_hi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "26347",
                    "1.13 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_hi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "31689",
                    "1.34 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_hi_all-records_labels.zip", "57857", "2.66 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_hi_all-records_labels.zip", "97609", "4.13 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_hi_all-records_labels.zip", "44868", "1.52 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_hi_all-records_labels.zip", "48255", "2.42 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_hi_all-records_labels.zip", "39152", "1.81 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_hi_all-records_labels.zip", "58044", "2.51 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_hi_all-records_labels.zip", "72505", "2.88 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_hi_all-records_labels.zip", "52036", "2.39 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_hi_all-records_labels.zip", "57360", "2.61 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_hi_all-records_labels.zip", "62718", "2.93 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_hi_all-records_labels.zip", "69807", "3.22 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_hi_originated-records_labels.zip",
                    "32822",
                    "1.42 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_hi_originated-records_labels.zip",
                    "39270",
                    "1.64 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_hi_originated-records_labels.zip",
                    "26553",
                    "842.99 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_hi_originated-records_labels.zip",
                    "28778",
                    "1.34 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_hi_originated-records_labels.zip",
                    "22377",
                    "977.23 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_hi_originated-records_labels.zip",
                    "25770",
                    "1.07 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_hi_originated-records_labels.zip",
                    "36594",
                    "1.37 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_hi_originated-records_labels.zip",
                    "27526",
                    "1.18 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_hi_originated-records_labels.zip",
                    "29807",
                    "1.25 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_hi_originated-records_labels.zip",
                    "36581",
                    "1.6 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_hi_originated-records_labels.zip",
                    "40668",
                    "1.75 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_hi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "25790",
                    "747.28 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_hi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "26443",
                    "769.57 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_hi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "20146",
                    "442.43 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_hi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "21679",
                    "682.34 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_hi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "16100",
                    "467.14 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_hi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "19577",
                    "565.45 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_hi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "31476",
                    "829.34 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_hi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "22003",
                    "617.15 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_hi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "24636",
                    "682.86 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_hi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "26347",
                    "767.75 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_hi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "31689",
                    "898.68 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_hi_all-records_codes.zip", "57857", "1.73 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_hi_all-records_codes.zip", "97609", "2.81 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_hi_all-records_codes.zip", "44868", "991.92 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_hi_all-records_codes.zip", "48255", "1.59 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_hi_all-records_codes.zip", "39152", "1.17 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_hi_all-records_codes.zip", "58044", "1.7 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_hi_all-records_codes.zip", "72505", "1.97 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_hi_all-records_codes.zip", "52036", "1.54 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_hi_all-records_codes.zip", "57360", "1.69 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_hi_all-records_codes.zip", "62718", "1.9 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_hi_all-records_codes.zip", "69807", "2.09 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_hi_originated-records_codes.zip",
                    "32822",
                    "955.73 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_hi_originated-records_codes.zip",
                    "39270",
                    "1.15 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_hi_originated-records_codes.zip",
                    "26553",
                    "577.19 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_hi_originated-records_codes.zip",
                    "28778",
                    "909.22 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_hi_originated-records_codes.zip",
                    "22377",
                    "650.88 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_hi_originated-records_codes.zip",
                    "25770",
                    "741.44 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_hi_originated-records_codes.zip",
                    "36594",
                    "946.61 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_hi_originated-records_codes.zip",
                    "27526",
                    "777.03 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_hi_originated-records_codes.zip",
                    "29807",
                    "833.67 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_hi_originated-records_codes.zip",
                    "36581",
                    "1.06 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_hi_originated-records_codes.zip",
                    "40668",
                    "1.17 MB",
                ),
            },
        },
    },
    "ok": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ok_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "61711",
                    "2.99 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ok_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "71771",
                    "3.36 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ok_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "56021",
                    "1.71 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ok_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "57409",
                    "3.04 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ok_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "53820",
                    "2.56 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ok_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "64839",
                    "3.04 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ok_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "83962",
                    "3.72 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ok_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "62083",
                    "2.92 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ok_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "68205",
                    "3.24 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ok_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "68275",
                    "3.28 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ok_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "77297",
                    "3.66 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ok_all-records_labels.zip", "165463", "8.55 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ok_all-records_labels.zip", "250763", "12.15 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ok_all-records_labels.zip", "150838", "5.09 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ok_all-records_labels.zip", "152804", "8.67 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ok_all-records_labels.zip", "146824", "7.59 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ok_all-records_labels.zip", "194552", "9.58 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ok_all-records_labels.zip", "219393", "10.29 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ok_all-records_labels.zip", "163798", "8.6 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ok_all-records_labels.zip", "177023", "9.25 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ok_all-records_labels.zip", "180860", "9.5 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ok_all-records_labels.zip", "189005", "9.82 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ok_originated-records_labels.zip",
                    "84730",
                    "4.21 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ok_originated-records_labels.zip",
                    "107739",
                    "5.16 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ok_originated-records_labels.zip",
                    "78302",
                    "2.43 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ok_originated-records_labels.zip",
                    "79611",
                    "4.27 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ok_originated-records_labels.zip",
                    "76088",
                    "3.74 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ok_originated-records_labels.zip",
                    "90679",
                    "4.34 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ok_originated-records_labels.zip",
                    "105102",
                    "4.8 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ok_originated-records_labels.zip",
                    "81562",
                    "3.94 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ok_originated-records_labels.zip",
                    "87420",
                    "4.24 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ok_originated-records_labels.zip",
                    "91830",
                    "4.49 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ok_originated-records_labels.zip",
                    "98582",
                    "4.73 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ok_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "61711",
                    "2.07 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ok_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "71771",
                    "2.36 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ok_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "56021",
                    "1.24 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ok_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "57409",
                    "2.11 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ok_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "53820",
                    "1.76 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ok_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "64839",
                    "2.14 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ok_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "83962",
                    "2.65 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ok_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "62083",
                    "1.97 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ok_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "68205",
                    "2.2 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ok_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "68275",
                    "2.25 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ok_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "77297",
                    "2.49 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ok_all-records_codes.zip", "165463", "5.67 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ok_all-records_codes.zip", "250763", "8.32 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ok_all-records_codes.zip", "150838", "3.38 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ok_all-records_codes.zip", "152804", "5.81 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ok_all-records_codes.zip", "146824", "5.04 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ok_all-records_codes.zip", "194552", "6.58 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ok_all-records_codes.zip", "219393", "7.12 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ok_all-records_codes.zip", "163798", "5.66 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ok_all-records_codes.zip", "177023", "6.13 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ok_all-records_codes.zip", "180860", "6.33 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ok_all-records_codes.zip", "189005", "6.53 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ok_originated-records_codes.zip",
                    "84730",
                    "2.89 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ok_originated-records_codes.zip",
                    "107739",
                    "3.62 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ok_originated-records_codes.zip",
                    "78302",
                    "1.73 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ok_originated-records_codes.zip",
                    "79611",
                    "2.95 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ok_originated-records_codes.zip",
                    "76088",
                    "2.55 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ok_originated-records_codes.zip",
                    "90679",
                    "3.04 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ok_originated-records_codes.zip",
                    "105102",
                    "3.39 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ok_originated-records_codes.zip",
                    "81562",
                    "2.64 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ok_originated-records_codes.zip",
                    "87420",
                    "2.87 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ok_originated-records_codes.zip",
                    "91830",
                    "3.05 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ok_originated-records_codes.zip",
                    "98582",
                    "3.19 MB",
                ),
            },
        },
    },
    "fl": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_fl_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "415338",
                    "21.43 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_fl_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "501111",
                    "25.12 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_fl_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "396688",
                    "13.19 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_fl_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "347883",
                    "21.05 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_fl_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "272904",
                    "13.99 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_fl_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "258117",
                    "12.67 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_fl_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "263772",
                    "12.4 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_fl_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "231239",
                    "11.59 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_fl_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "240644",
                    "12.01 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_fl_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "365896",
                    "19.08 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_fl_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "373288",
                    "19.2 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_fl_all-records_labels.zip", "1043942", "58 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_fl_all-records_labels.zip",
                    "2006660",
                    "102.81 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_fl_all-records_labels.zip",
                    "1018763",
                    "38.28 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_fl_all-records_labels.zip", "893206", "57.89 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_fl_all-records_labels.zip", "732825", "40.79 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_fl_all-records_labels.zip", "962944", "49.47 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_fl_all-records_labels.zip", "806975", "40.26 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_fl_all-records_labels.zip", "647776", "35.66 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_fl_all-records_labels.zip", "675688", "37.38 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_fl_all-records_labels.zip", "948672", "53.81 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_fl_all-records_labels.zip", "919923", "51.66 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_fl_originated-records_labels.zip",
                    "506394",
                    "26.46 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_fl_originated-records_labels.zip",
                    "735174",
                    "36.57 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_fl_originated-records_labels.zip",
                    "492702",
                    "16.61 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_fl_originated-records_labels.zip",
                    "434779",
                    "26.78 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_fl_originated-records_labels.zip",
                    "349696",
                    "18.14 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_fl_originated-records_labels.zip",
                    "344859",
                    "17 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_fl_originated-records_labels.zip",
                    "318689",
                    "15.06 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_fl_originated-records_labels.zip",
                    "288632",
                    "14.64 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_fl_originated-records_labels.zip",
                    "292476",
                    "14.8 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_fl_originated-records_labels.zip",
                    "467201",
                    "24.7 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_fl_originated-records_labels.zip",
                    "462049",
                    "24.13 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_fl_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "415338",
                    "15.17 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_fl_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "501111",
                    "17.95 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_fl_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "396688",
                    "9.14 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_fl_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "347883",
                    "14.62 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_fl_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "272904",
                    "9.87 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_fl_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "258117",
                    "8.93 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_fl_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "263772",
                    "8.88 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_fl_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "231239",
                    "8 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_fl_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "240644",
                    "8.28 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_fl_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "365896",
                    "13.41 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_fl_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "373288",
                    "13.48 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_fl_all-records_codes.zip", "1043942", "40.03 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_fl_all-records_codes.zip", "2006660", "71.9 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_fl_all-records_codes.zip", "1018763", "24.91 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_fl_all-records_codes.zip", "893206", "38.26 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_fl_all-records_codes.zip", "732825", "28.16 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_fl_all-records_codes.zip", "962944", "34.41 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_fl_all-records_codes.zip", "806975", "28.11 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_fl_all-records_codes.zip", "647776", "23.83 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_fl_all-records_codes.zip", "675688", "24.98 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_fl_all-records_codes.zip", "948672", "36.68 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_fl_all-records_codes.zip", "919923", "35.16 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_fl_originated-records_codes.zip",
                    "506394",
                    "18.65 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_fl_originated-records_codes.zip",
                    "735174",
                    "26.09 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_fl_originated-records_codes.zip",
                    "492702",
                    "11.34 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_fl_originated-records_codes.zip",
                    "434779",
                    "18.42 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_fl_originated-records_codes.zip",
                    "349696",
                    "12.69 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_fl_originated-records_codes.zip",
                    "344859",
                    "11.94 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_fl_originated-records_codes.zip",
                    "318689",
                    "10.73 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_fl_originated-records_codes.zip",
                    "288632",
                    "10.03 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_fl_originated-records_codes.zip",
                    "292476",
                    "10.16 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_fl_originated-records_codes.zip",
                    "467201",
                    "17.24 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_fl_originated-records_codes.zip",
                    "462049",
                    "16.84 MB",
                ),
            },
        },
    },
    "wy": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wy_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12342",
                    "483.6 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wy_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "13857",
                    "521.55 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wy_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "10510",
                    "270.62 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wy_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "11880",
                    "503.22 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wy_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "10422",
                    "425.8 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wy_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12387",
                    "474.69 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wy_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "16912",
                    "594.41 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wy_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "11423",
                    "470.67 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wy_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12694",
                    "489.69 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wy_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "14178",
                    "537.95 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wy_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15410",
                    "568.4 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wy_all-records_labels.zip", "30163", "1.29 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wy_all-records_labels.zip", "48234", "1.94 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wy_all-records_labels.zip", "26154", "743.51 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wy_all-records_labels.zip", "28641", "1.34 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wy_all-records_labels.zip", "25049", "1.13 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wy_all-records_labels.zip", "35748", "1.45 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wy_all-records_labels.zip", "41659", "1.59 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wy_all-records_labels.zip", "28465", "1.31 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wy_all-records_labels.zip", "32035", "1.37 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wy_all-records_labels.zip", "32956", "1.37 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wy_all-records_labels.zip", "34092", "1.4 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wy_originated-records_labels.zip",
                    "15484",
                    "616.35 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wy_originated-records_labels.zip",
                    "21052",
                    "815.34 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wy_originated-records_labels.zip",
                    "13702",
                    "356.27 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wy_originated-records_labels.zip",
                    "15107",
                    "651.6 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wy_originated-records_labels.zip",
                    "13556",
                    "566.41 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wy_originated-records_labels.zip",
                    "16892",
                    "658.73 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wy_originated-records_labels.zip",
                    "20290",
                    "727.57 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wy_originated-records_labels.zip",
                    "14507",
                    "613.35 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wy_originated-records_labels.zip",
                    "15602",
                    "616.08 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wy_originated-records_labels.zip",
                    "17900",
                    "691.83 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wy_originated-records_labels.zip",
                    "19114",
                    "723.04 KB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wy_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12342",
                    "312.27 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wy_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "13857",
                    "338.82 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wy_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "10510",
                    "187.36 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wy_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "11880",
                    "319.17 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wy_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "10422",
                    "275.68 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wy_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12387",
                    "309.95 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wy_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "16912",
                    "397.25 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wy_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "11423",
                    "302.39 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wy_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12694",
                    "313.52 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wy_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "14178",
                    "348.1 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wy_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15410",
                    "368.87 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wy_all-records_codes.zip", "30163", "802.03 KB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wy_all-records_codes.zip", "48234", "1.23 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wy_all-records_codes.zip", "26154", "481.64 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wy_all-records_codes.zip", "28641", "812.32 KB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wy_all-records_codes.zip", "25049", "695.65 KB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wy_all-records_codes.zip", "35748", "923.02 KB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wy_all-records_codes.zip", "41659", "1.02 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wy_all-records_codes.zip", "28465", "807.3 KB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wy_all-records_codes.zip", "32035", "844.63 KB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wy_all-records_codes.zip", "32956", "857.37 KB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wy_all-records_codes.zip", "34092", "878.55 KB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_wy_originated-records_codes.zip",
                    "15484",
                    "395.6 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_wy_originated-records_codes.zip",
                    "21052",
                    "528.23 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_wy_originated-records_codes.zip",
                    "13702",
                    "246.43 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_wy_originated-records_codes.zip",
                    "15107",
                    "410.78 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_wy_originated-records_codes.zip",
                    "13556",
                    "363.31 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_wy_originated-records_codes.zip",
                    "16892",
                    "430.54 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_wy_originated-records_codes.zip",
                    "20290",
                    "484.44 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_wy_originated-records_codes.zip",
                    "14507",
                    "390.89 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_wy_originated-records_codes.zip",
                    "15602",
                    "393.56 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_wy_originated-records_codes.zip",
                    "17900",
                    "445.73 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_wy_originated-records_codes.zip",
                    "19114",
                    "467.43 KB",
                ),
            },
        },
    },
    "me": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_me_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "25576",
                    "1.12 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_me_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "28469",
                    "1.25 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_me_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "23089",
                    "660.63 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_me_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "22073",
                    "1.06 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_me_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "18699",
                    "819.03 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_me_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "23318",
                    "1.01 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_me_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "35977",
                    "1.45 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_me_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "24858",
                    "1.05 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_me_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "29685",
                    "1.3 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_me_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "28892",
                    "1.25 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_me_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "32810",
                    "1.4 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_me_all-records_labels.zip", "64142", "3.02 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_me_all-records_labels.zip", "102877", "4.79 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_me_all-records_labels.zip", "58188", "1.77 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_me_all-records_labels.zip", "56450", "2.96 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_me_all-records_labels.zip", "50231", "2.36 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_me_all-records_labels.zip", "74281", "3.56 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_me_all-records_labels.zip", "88765", "4 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_me_all-records_labels.zip", "65903", "3.22 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_me_all-records_labels.zip", "75911", "3.76 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_me_all-records_labels.zip", "71008", "3.35 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_me_all-records_labels.zip", "79176", "3.7 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_me_originated-records_labels.zip",
                    "33761",
                    "1.53 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_me_originated-records_labels.zip",
                    "44333",
                    "2.01 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_me_originated-records_labels.zip",
                    "31503",
                    "929.28 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_me_originated-records_labels.zip",
                    "29602",
                    "1.45 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_me_originated-records_labels.zip",
                    "25962",
                    "1.19 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_me_originated-records_labels.zip",
                    "34638",
                    "1.54 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_me_originated-records_labels.zip",
                    "45092",
                    "1.88 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_me_originated-records_labels.zip",
                    "32181",
                    "1.43 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_me_originated-records_labels.zip",
                    "37475",
                    "1.73 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_me_originated-records_labels.zip",
                    "37720",
                    "1.67 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_me_originated-records_labels.zip",
                    "41515",
                    "1.82 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_me_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "25576",
                    "725.36 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_me_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "28469",
                    "820.97 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_me_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "23089",
                    "468.44 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_me_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "22073",
                    "702.08 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_me_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "18699",
                    "527.54 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_me_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "23318",
                    "660.77 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_me_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "35977",
                    "975.94 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_me_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "24858",
                    "674.23 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_me_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "29685",
                    "841.65 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_me_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "28892",
                    "797.28 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_me_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "32810",
                    "894.15 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_me_all-records_codes.zip", "64142", "1.89 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_me_all-records_codes.zip", "102877", "3.1 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_me_all-records_codes.zip", "58188", "1.16 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_me_all-records_codes.zip", "56450", "1.88 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_me_all-records_codes.zip", "50231", "1.46 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_me_all-records_codes.zip", "74281", "2.32 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_me_all-records_codes.zip", "88765", "2.65 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_me_all-records_codes.zip", "65903", "2.01 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_me_all-records_codes.zip", "75911", "2.35 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_me_all-records_codes.zip", "71008", "2.07 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_me_all-records_codes.zip", "79176", "2.29 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_me_originated-records_codes.zip",
                    "33761",
                    "987 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_me_originated-records_codes.zip",
                    "44333",
                    "1.33 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_me_originated-records_codes.zip",
                    "31503",
                    "654.38 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_me_originated-records_codes.zip",
                    "29602",
                    "954.33 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_me_originated-records_codes.zip",
                    "25962",
                    "765.27 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_me_originated-records_codes.zip",
                    "34638",
                    "1.02 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_me_originated-records_codes.zip",
                    "45092",
                    "1.26 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_me_originated-records_codes.zip",
                    "32181",
                    "909.63 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_me_originated-records_codes.zip",
                    "37475",
                    "1.11 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_me_originated-records_codes.zip",
                    "37720",
                    "1.06 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_me_originated-records_codes.zip",
                    "41515",
                    "1.15 MB",
                ),
            },
        },
    },
    "md": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_md_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "151314",
                    "7.51 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_md_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "189965",
                    "9.14 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_md_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "124206",
                    "4 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_md_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "131786",
                    "7.26 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_md_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "98965",
                    "5.23 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_md_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "133536",
                    "6.34 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_md_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "193122",
                    "8.53 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_md_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "142588",
                    "7.11 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_md_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "166872",
                    "8.22 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_md_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "161491",
                    "8.05 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_md_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "195908",
                    "9.85 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_md_all-records_labels.zip", "358958", "19.06 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_md_all-records_labels.zip", "656616", "31.96 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_md_all-records_labels.zip", "301879", "10.75 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_md_all-records_labels.zip", "316012", "18.68 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_md_all-records_labels.zip", "247561", "14.04 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_md_all-records_labels.zip", "393039", "19.26 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_md_all-records_labels.zip", "467697", "21.73 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_md_all-records_labels.zip", "347645", "18.89 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_md_all-records_labels.zip", "385128", "20.7 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_md_all-records_labels.zip", "385383", "20.95 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_md_all-records_labels.zip", "439566", "23.91 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_md_originated-records_labels.zip",
                    "171556",
                    "8.64 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_md_originated-records_labels.zip",
                    "261984",
                    "12.73 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_md_originated-records_labels.zip",
                    "144610",
                    "4.78 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_md_originated-records_labels.zip",
                    "152541",
                    "8.53 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_md_originated-records_labels.zip",
                    "118429",
                    "6.33 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_md_originated-records_labels.zip",
                    "162234",
                    "7.83 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_md_originated-records_labels.zip",
                    "210794",
                    "9.48 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_md_originated-records_labels.zip",
                    "159707",
                    "8.13 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_md_originated-records_labels.zip",
                    "182102",
                    "9.04 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_md_originated-records_labels.zip",
                    "187825",
                    "9.46 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_md_originated-records_labels.zip",
                    "219387",
                    "11.11 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_md_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "151314",
                    "5.32 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_md_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "189965",
                    "6.47 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_md_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "124206",
                    "2.79 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_md_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "131786",
                    "5.19 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_md_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "98965",
                    "3.67 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_md_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "133536",
                    "4.46 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_md_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "193122",
                    "6.08 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_md_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "142588",
                    "4.91 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_md_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "166872",
                    "5.7 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_md_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "161491",
                    "5.68 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_md_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "195908",
                    "6.88 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_md_all-records_codes.zip", "358958", "13.18 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_md_all-records_codes.zip", "656616", "22.08 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_md_all-records_codes.zip", "301879", "6.99 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_md_all-records_codes.zip", "316012", "12.83 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_md_all-records_codes.zip", "247561", "9.61 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_md_all-records_codes.zip", "393039", "13.28 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_md_all-records_codes.zip", "467697", "15.2 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_md_all-records_codes.zip", "347645", "12.83 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_md_all-records_codes.zip", "385128", "14.08 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_md_all-records_codes.zip", "385383", "14.56 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_md_all-records_codes.zip", "439566", "16.52 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_md_originated-records_codes.zip",
                    "171556",
                    "6.1 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_md_originated-records_codes.zip",
                    "261984",
                    "9.04 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_md_originated-records_codes.zip",
                    "144610",
                    "3.3 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_md_originated-records_codes.zip",
                    "152541",
                    "6.06 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_md_originated-records_codes.zip",
                    "118429",
                    "4.41 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_md_originated-records_codes.zip",
                    "162234",
                    "5.51 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_md_originated-records_codes.zip",
                    "210794",
                    "6.75 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_md_originated-records_codes.zip",
                    "159707",
                    "5.59 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_md_originated-records_codes.zip",
                    "182102",
                    "6.24 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_md_originated-records_codes.zip",
                    "187825",
                    "6.64 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_md_originated-records_codes.zip",
                    "219387",
                    "7.7 MB",
                ),
            },
        },
    },
    "ma": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ma_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "168663",
                    "8.43 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ma_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "148532",
                    "7.1 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ma_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "129891",
                    "4.16 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ma_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "144027",
                    "7.64 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ma_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "109057",
                    "5.41 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ma_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "126855",
                    "6.11 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ma_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "229420",
                    "10.04 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ma_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "177890",
                    "8.46 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ma_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "212589",
                    "10.01 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ma_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "186856",
                    "9.2 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ma_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "252396",
                    "12.13 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ma_all-records_labels.zip", "350131", "18.93 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ma_all-records_labels.zip", "507509", "24.85 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ma_all-records_labels.zip", "282546", "10.31 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ma_all-records_labels.zip", "299991", "17.01 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ma_all-records_labels.zip", "246533", "13.15 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ma_all-records_labels.zip", "337077", "17.11 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ma_all-records_labels.zip", "493549", "22.81 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ma_all-records_labels.zip", "400586", "20.86 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ma_all-records_labels.zip", "458768", "23.77 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ma_all-records_labels.zip", "405166", "21.77 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ma_all-records_labels.zip", "516205", "27.13 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ma_originated-records_labels.zip",
                    "201756",
                    "10.26 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ma_originated-records_labels.zip",
                    "214170",
                    "10.35 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ma_originated-records_labels.zip",
                    "162474",
                    "5.34 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ma_originated-records_labels.zip",
                    "173355",
                    "9.34 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ma_originated-records_labels.zip",
                    "137873",
                    "6.99 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ma_originated-records_labels.zip",
                    "159312",
                    "7.79 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ma_originated-records_labels.zip",
                    "255679",
                    "11.37 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ma_originated-records_labels.zip",
                    "205164",
                    "9.93 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ma_originated-records_labels.zip",
                    "239023",
                    "11.5 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ma_originated-records_labels.zip",
                    "224809",
                    "11.32 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ma_originated-records_labels.zip",
                    "288584",
                    "14 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ma_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "168663",
                    "5.88 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ma_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "148532",
                    "5 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ma_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "129891",
                    "2.95 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ma_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "144027",
                    "5.53 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ma_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "109057",
                    "3.83 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ma_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "126855",
                    "4.32 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ma_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "229420",
                    "7.29 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ma_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "177890",
                    "5.8 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ma_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "212589",
                    "6.88 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ma_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "186856",
                    "6.35 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ma_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "252396",
                    "8.35 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ma_all-records_codes.zip", "350131", "13.03 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ma_all-records_codes.zip", "507509", "17.13 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ma_all-records_codes.zip", "282546", "6.92 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ma_all-records_codes.zip", "299991", "11.87 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ma_all-records_codes.zip", "246533", "9.05 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ma_all-records_codes.zip", "337077", "11.88 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ma_all-records_codes.zip", "493549", "16.23 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ma_all-records_codes.zip", "400586", "14.19 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ma_all-records_codes.zip", "458768", "16.27 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ma_all-records_codes.zip", "405166", "14.9 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ma_all-records_codes.zip", "516205", "18.65 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ma_originated-records_codes.zip",
                    "201756",
                    "7.12 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ma_originated-records_codes.zip",
                    "214170",
                    "7.34 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ma_originated-records_codes.zip",
                    "162474",
                    "3.73 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ma_originated-records_codes.zip",
                    "173355",
                    "6.7 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ma_originated-records_codes.zip",
                    "137873",
                    "4.9 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ma_originated-records_codes.zip",
                    "159312",
                    "5.51 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ma_originated-records_codes.zip",
                    "255679",
                    "8.23 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ma_originated-records_codes.zip",
                    "205164",
                    "6.77 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ma_originated-records_codes.zip",
                    "239023",
                    "7.91 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ma_originated-records_codes.zip",
                    "224809",
                    "7.79 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ma_originated-records_codes.zip",
                    "288584",
                    "9.58 MB",
                ),
            },
        },
    },
    "oh": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_oh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "232207",
                    "11.88 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_oh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "224598",
                    "11.06 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_oh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "208362",
                    "6.69 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_oh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "204738",
                    "11.72 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_oh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "174084",
                    "8.93 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_oh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "186092",
                    "9.03 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_oh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "282249",
                    "12.44 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_oh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "219789",
                    "10.95 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_oh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "258240",
                    "12.72 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_oh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "267654",
                    "13.76 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_oh_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "302970",
                    "15.14 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_oh_all-records_labels.zip", "493271", "27.33 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_oh_all-records_labels.zip", "774401", "39.17 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_oh_all-records_labels.zip", "448269", "16.35 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_oh_all-records_labels.zip", "439676", "27.18 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_oh_all-records_labels.zip", "394459", "21.93 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_oh_all-records_labels.zip", "533639", "27.2 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_oh_all-records_labels.zip", "624555", "29.69 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_oh_all-records_labels.zip", "489066", "26.92 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_oh_all-records_labels.zip", "555119", "30.3 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_oh_all-records_labels.zip", "578940", "32.56 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_oh_all-records_labels.zip", "618867", "34.01 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_oh_originated-records_labels.zip",
                    "262449",
                    "13.71 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_oh_originated-records_labels.zip",
                    "313279",
                    "15.77 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_oh_originated-records_labels.zip",
                    "241167",
                    "7.96 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_oh_originated-records_labels.zip",
                    "235058",
                    "13.65 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_oh_originated-records_labels.zip",
                    "203927",
                    "10.71 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_oh_originated-records_labels.zip",
                    "231697",
                    "11.5 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_oh_originated-records_labels.zip",
                    "309496",
                    "13.92 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_oh_originated-records_labels.zip",
                    "245688",
                    "12.6 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_oh_originated-records_labels.zip",
                    "283698",
                    "14.38 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_oh_originated-records_labels.zip",
                    "306698",
                    "15.95 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_oh_originated-records_labels.zip",
                    "336141",
                    "16.99 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_oh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "232207",
                    "8.28 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_oh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "224598",
                    "7.85 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_oh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "208362",
                    "4.84 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_oh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "204738",
                    "8.2 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_oh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "174084",
                    "6.26 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_oh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "186092",
                    "6.43 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_oh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "282249",
                    "9.02 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_oh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "219789",
                    "7.49 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_oh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "258240",
                    "8.73 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_oh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "267654",
                    "9.51 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_oh_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "302970",
                    "10.48 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_oh_all-records_codes.zip", "493271", "18.52 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_oh_all-records_codes.zip", "774401", "27.06 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_oh_all-records_codes.zip", "448269", "10.89 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_oh_all-records_codes.zip", "439676", "18.32 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_oh_all-records_codes.zip", "394459", "14.89 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_oh_all-records_codes.zip", "533639", "18.82 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_oh_all-records_codes.zip", "624555", "20.88 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_oh_all-records_codes.zip", "489066", "17.97 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_oh_all-records_codes.zip", "555119", "20.35 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_oh_all-records_codes.zip", "578940", "22.01 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_oh_all-records_codes.zip", "618867", "23.02 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_oh_originated-records_codes.zip",
                    "262449",
                    "9.52 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_oh_originated-records_codes.zip",
                    "313279",
                    "11.21 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_oh_originated-records_codes.zip",
                    "241167",
                    "5.68 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_oh_originated-records_codes.zip",
                    "235058",
                    "9.5 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_oh_originated-records_codes.zip",
                    "203927",
                    "7.49 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_oh_originated-records_codes.zip",
                    "231697",
                    "8.17 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_oh_originated-records_codes.zip",
                    "309496",
                    "10.06 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_oh_originated-records_codes.zip",
                    "245688",
                    "8.63 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_oh_originated-records_codes.zip",
                    "283698",
                    "9.88 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_oh_originated-records_codes.zip",
                    "306698",
                    "10.96 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_oh_originated-records_codes.zip",
                    "336141",
                    "11.68 MB",
                ),
            },
        },
    },
    "ut": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ut_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "106374",
                    "4.72 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ut_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "94558",
                    "4.04 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ut_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "87920",
                    "2.62 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ut_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "88686",
                    "4.42 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ut_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "62864",
                    "2.8 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ut_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "83133",
                    "3.43 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ut_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "117282",
                    "4.64 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ut_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "66630",
                    "2.88 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ut_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "90322",
                    "3.86 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ut_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "82759",
                    "3.71 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ut_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "108573",
                    "4.87 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ut_all-records_labels.zip", "227871", "11.21 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ut_all-records_labels.zip", "319327", "14.16 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ut_all-records_labels.zip", "198425", "6.62 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ut_all-records_labels.zip", "192509", "10.37 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ut_all-records_labels.zip", "144848", "7.1 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ut_all-records_labels.zip", "226654", "9.81 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ut_all-records_labels.zip", "279791", "11.41 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ut_all-records_labels.zip", "166439", "7.98 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ut_all-records_labels.zip", "212181", "10.08 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ut_all-records_labels.zip", "192653", "9.53 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ut_all-records_labels.zip", "230544", "11.39 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ut_originated-records_labels.zip",
                    "126325",
                    "5.77 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ut_originated-records_labels.zip",
                    "136628",
                    "5.96 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ut_originated-records_labels.zip",
                    "108018",
                    "3.29 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ut_originated-records_labels.zip",
                    "105929",
                    "5.36 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ut_originated-records_labels.zip",
                    "76563",
                    "3.49 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ut_originated-records_labels.zip",
                    "98555",
                    "4.16 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ut_originated-records_labels.zip",
                    "127680",
                    "5.13 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ut_originated-records_labels.zip",
                    "77763",
                    "3.46 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ut_originated-records_labels.zip",
                    "101108",
                    "4.4 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ut_originated-records_labels.zip",
                    "99424",
                    "4.53 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ut_originated-records_labels.zip",
                    "125331",
                    "5.73 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ut_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "106374",
                    "3.15 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ut_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "94558",
                    "2.78 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ut_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "87920",
                    "1.85 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ut_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "88686",
                    "3.08 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ut_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "62864",
                    "1.88 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ut_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "83133",
                    "2.4 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ut_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "117282",
                    "3.31 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ut_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "66630",
                    "1.92 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ut_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "90322",
                    "2.56 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ut_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "82759",
                    "2.48 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ut_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "108573",
                    "3.28 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ut_all-records_codes.zip", "227871", "7.32 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ut_all-records_codes.zip", "319327", "9.65 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ut_all-records_codes.zip", "198425", "4.41 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ut_all-records_codes.zip", "192509", "6.96 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ut_all-records_codes.zip", "144848", "4.66 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ut_all-records_codes.zip", "226654", "6.76 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ut_all-records_codes.zip", "279791", "7.94 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ut_all-records_codes.zip", "166439", "5.23 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ut_all-records_codes.zip", "212181", "6.6 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ut_all-records_codes.zip", "192653", "6.29 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ut_all-records_codes.zip", "230544", "7.57 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ut_originated-records_codes.zip",
                    "126325",
                    "3.86 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ut_originated-records_codes.zip",
                    "136628",
                    "4.14 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ut_originated-records_codes.zip",
                    "108018",
                    "2.31 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ut_originated-records_codes.zip",
                    "105929",
                    "3.72 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ut_originated-records_codes.zip",
                    "76563",
                    "2.34 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ut_originated-records_codes.zip",
                    "98555",
                    "2.91 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ut_originated-records_codes.zip",
                    "127680",
                    "3.64 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ut_originated-records_codes.zip",
                    "77763",
                    "2.3 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ut_originated-records_codes.zip",
                    "101108",
                    "2.91 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ut_originated-records_codes.zip",
                    "99424",
                    "3.03 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ut_originated-records_codes.zip",
                    "125331",
                    "3.84 MB",
                ),
            },
        },
    },
    "mo": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mo_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "139247",
                    "6.75 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mo_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "154268",
                    "7.4 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mo_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "118901",
                    "3.83 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mo_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "121654",
                    "6.63 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mo_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "95718",
                    "4.8 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mo_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "132777",
                    "6.15 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mo_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "186579",
                    "8.07 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mo_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "130134",
                    "6.22 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mo_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "158585",
                    "7.57 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mo_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "146638",
                    "7.2 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mo_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "175614",
                    "8.39 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mo_all-records_labels.zip", "312237", "16.09 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mo_all-records_labels.zip", "531617", "25.33 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mo_all-records_labels.zip", "277843", "9.61 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mo_all-records_labels.zip", "276661", "16.28 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mo_all-records_labels.zip", "232023", "12.42 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mo_all-records_labels.zip", "379587", "17.83 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mo_all-records_labels.zip", "447918", "19.75 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mo_all-records_labels.zip", "309645", "15.9 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mo_all-records_labels.zip", "360738", "18.59 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mo_all-records_labels.zip", "347186", "18.19 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mo_all-records_labels.zip", "384551", "19.69 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mo_originated-records_labels.zip",
                    "165943",
                    "8.21 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mo_originated-records_labels.zip",
                    "218490",
                    "10.7 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mo_originated-records_labels.zip",
                    "145419",
                    "4.81 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mo_originated-records_labels.zip",
                    "147519",
                    "8.15 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mo_originated-records_labels.zip",
                    "120463",
                    "6.22 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mo_originated-records_labels.zip",
                    "169405",
                    "8.03 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mo_originated-records_labels.zip",
                    "211924",
                    "9.41 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mo_originated-records_labels.zip",
                    "154134",
                    "7.55 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mo_originated-records_labels.zip",
                    "182546",
                    "8.84 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mo_originated-records_labels.zip",
                    "178486",
                    "8.86 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mo_originated-records_labels.zip",
                    "204935",
                    "9.93 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mo_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "139247",
                    "4.66 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mo_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "154268",
                    "5.21 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mo_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "118901",
                    "2.73 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mo_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "121654",
                    "4.64 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mo_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "95718",
                    "3.31 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mo_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "132777",
                    "4.34 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mo_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "186579",
                    "5.81 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mo_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "130134",
                    "4.23 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mo_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "158585",
                    "5.17 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mo_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "146638",
                    "4.98 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mo_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "175614",
                    "5.75 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mo_all-records_codes.zip", "312237", "10.71 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mo_all-records_codes.zip", "531617", "17.33 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mo_all-records_codes.zip", "277843", "6.33 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mo_all-records_codes.zip", "276661", "10.94 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mo_all-records_codes.zip", "232023", "8.21 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mo_all-records_codes.zip", "379587", "12.23 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mo_all-records_codes.zip", "447918", "13.74 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mo_all-records_codes.zip", "309645", "10.46 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mo_all-records_codes.zip", "360738", "12.3 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mo_all-records_codes.zip", "347186", "12.14 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mo_all-records_codes.zip", "384551", "13.07 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mo_originated-records_codes.zip",
                    "165943",
                    "5.62 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mo_originated-records_codes.zip",
                    "218490",
                    "7.52 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mo_originated-records_codes.zip",
                    "145419",
                    "3.37 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mo_originated-records_codes.zip",
                    "147519",
                    "5.65 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mo_originated-records_codes.zip",
                    "120463",
                    "4.26 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mo_originated-records_codes.zip",
                    "169405",
                    "5.64 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mo_originated-records_codes.zip",
                    "211924",
                    "6.73 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mo_originated-records_codes.zip",
                    "154134",
                    "5.1 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mo_originated-records_codes.zip",
                    "182546",
                    "5.99 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mo_originated-records_codes.zip",
                    "178486",
                    "6.06 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mo_originated-records_codes.zip",
                    "204935",
                    "6.74 MB",
                ),
            },
        },
    },
    "mn": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "150929",
                    "7.76 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "114958",
                    "5.46 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "127113",
                    "3.8 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "135112",
                    "7.39 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "100659",
                    "5.19 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "101137",
                    "4.61 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "172464",
                    "7.33 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "130723",
                    "6.42 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "155626",
                    "7.58 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "158942",
                    "7.98 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mn_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "195258",
                    "9.69 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mn_all-records_labels.zip", "308571", "16.84 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mn_all-records_labels.zip", "396721", "18.97 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mn_all-records_labels.zip", "269551", "8.68 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mn_all-records_labels.zip", "280012", "16.44 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mn_all-records_labels.zip", "220146", "12.02 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mn_all-records_labels.zip", "272913", "12.87 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mn_all-records_labels.zip", "379860", "16.84 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mn_all-records_labels.zip", "282982", "14.91 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mn_all-records_labels.zip", "332542", "17.42 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mn_all-records_labels.zip", "332594", "17.76 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mn_all-records_labels.zip", "382934", "20.31 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mn_originated-records_labels.zip",
                    "176922",
                    "9.23 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mn_originated-records_labels.zip",
                    "171217",
                    "8.27 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mn_originated-records_labels.zip",
                    "154164",
                    "4.74 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mn_originated-records_labels.zip",
                    "160605",
                    "8.94 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mn_originated-records_labels.zip",
                    "123374",
                    "6.47 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mn_originated-records_labels.zip",
                    "130815",
                    "6.14 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mn_originated-records_labels.zip",
                    "195958",
                    "8.53 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mn_originated-records_labels.zip",
                    "151782",
                    "7.55 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mn_originated-records_labels.zip",
                    "177556",
                    "8.84 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mn_originated-records_labels.zip",
                    "187475",
                    "9.52 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mn_originated-records_labels.zip",
                    "222116",
                    "11.23 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "150929",
                    "5.39 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "114958",
                    "3.87 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "127113",
                    "2.69 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "135112",
                    "5.14 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "100659",
                    "3.62 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "101137",
                    "3.28 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "172464",
                    "5.3 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "130723",
                    "4.45 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "155626",
                    "5.29 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "158942",
                    "5.58 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mn_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "195258",
                    "6.78 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mn_all-records_codes.zip", "308571", "11.31 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mn_all-records_codes.zip", "396721", "13.04 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mn_all-records_codes.zip", "269551", "5.62 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mn_all-records_codes.zip", "280012", "10.99 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mn_all-records_codes.zip", "220146", "8.1 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mn_all-records_codes.zip", "272913", "8.89 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mn_all-records_codes.zip", "379860", "11.74 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mn_all-records_codes.zip", "282982", "10.01 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mn_all-records_codes.zip", "332542", "11.73 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mn_all-records_codes.zip", "332594", "12.03 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mn_all-records_codes.zip", "382934", "13.81 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mn_originated-records_codes.zip",
                    "176922",
                    "6.37 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mn_originated-records_codes.zip",
                    "171217",
                    "5.84 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mn_originated-records_codes.zip",
                    "154164",
                    "3.32 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mn_originated-records_codes.zip",
                    "160605",
                    "6.15 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mn_originated-records_codes.zip",
                    "123374",
                    "4.48 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mn_originated-records_codes.zip",
                    "130815",
                    "4.36 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mn_originated-records_codes.zip",
                    "195958",
                    "6.13 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mn_originated-records_codes.zip",
                    "151782",
                    "5.2 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mn_originated-records_codes.zip",
                    "177556",
                    "6.12 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mn_originated-records_codes.zip",
                    "187475",
                    "6.6 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mn_originated-records_codes.zip",
                    "222116",
                    "7.82 MB",
                ),
            },
        },
    },
    "mi": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "225509",
                    "11.38 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "202641",
                    "10.01 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "200696",
                    "6.21 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "198320",
                    "11.13 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "162424",
                    "8.1 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "149102",
                    "7.25 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "194235",
                    "8.77 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "168948",
                    "8.4 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "175445",
                    "8.52 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "239554",
                    "11.94 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mi_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "274203",
                    "13.44 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mi_all-records_labels.zip", "470652", "25.31 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mi_all-records_labels.zip", "780713", "38.5 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mi_all-records_labels.zip", "437181", "14.82 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mi_all-records_labels.zip", "424672", "25.71 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mi_all-records_labels.zip", "361546", "19.18 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mi_all-records_labels.zip", "472702", "23.46 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mi_all-records_labels.zip", "504304", "23.62 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mi_all-records_labels.zip", "396764", "21.31 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mi_all-records_labels.zip", "419300", "22.02 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mi_all-records_labels.zip", "521030", "27.85 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mi_all-records_labels.zip", "573645", "30.22 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mi_originated-records_labels.zip",
                    "262757",
                    "13.58 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mi_originated-records_labels.zip",
                    "294627",
                    "14.81 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mi_originated-records_labels.zip",
                    "241945",
                    "7.74 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mi_originated-records_labels.zip",
                    "233520",
                    "13.34 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mi_originated-records_labels.zip",
                    "194126",
                    "9.91 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mi_originated-records_labels.zip",
                    "191860",
                    "9.52 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mi_originated-records_labels.zip",
                    "224166",
                    "10.41 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mi_originated-records_labels.zip",
                    "196360",
                    "10.06 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mi_originated-records_labels.zip",
                    "202252",
                    "10.19 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mi_originated-records_labels.zip",
                    "280253",
                    "14.18 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mi_originated-records_labels.zip",
                    "312194",
                    "15.55 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "225509",
                    "7.89 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "202641",
                    "7.07 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "200696",
                    "4.39 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "198320",
                    "7.82 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "162424",
                    "5.66 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "149102",
                    "5.08 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "194235",
                    "6.2 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "168948",
                    "5.72 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "175445",
                    "5.8 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "239554",
                    "8.26 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mi_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "274203",
                    "9.28 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mi_all-records_codes.zip", "470652", "16.94 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mi_all-records_codes.zip", "780713", "26.45 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mi_all-records_codes.zip", "437181", "9.61 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mi_all-records_codes.zip", "424672", "17.31 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mi_all-records_codes.zip", "361546", "12.87 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mi_all-records_codes.zip", "472702", "16.04 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mi_all-records_codes.zip", "504304", "16.25 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mi_all-records_codes.zip", "396764", "14.07 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mi_all-records_codes.zip", "419300", "14.52 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mi_all-records_codes.zip", "521030", "18.59 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mi_all-records_codes.zip", "573645", "20.21 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mi_originated-records_codes.zip",
                    "262757",
                    "9.39 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mi_originated-records_codes.zip",
                    "294627",
                    "10.53 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mi_originated-records_codes.zip",
                    "241945",
                    "5.41 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mi_originated-records_codes.zip",
                    "233520",
                    "9.29 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mi_originated-records_codes.zip",
                    "194126",
                    "6.88 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mi_originated-records_codes.zip",
                    "191860",
                    "6.67 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mi_originated-records_codes.zip",
                    "224166",
                    "7.37 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mi_originated-records_codes.zip",
                    "196360",
                    "6.83 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mi_originated-records_codes.zip",
                    "202252",
                    "6.96 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mi_originated-records_codes.zip",
                    "280253",
                    "9.73 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mi_originated-records_codes.zip",
                    "312194",
                    "10.66 MB",
                ),
            },
        },
    },
    "ri": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ri_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "22014",
                    "1 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ri_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "24278",
                    "1.09 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ri_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "19545",
                    "600.94 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ri_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "19238",
                    "896.87 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ri_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "14179",
                    "687.6 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ri_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "18140",
                    "802.68 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ri_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "29449",
                    "1.2 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ri_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "20369",
                    "903.7 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ri_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "24263",
                    "1.09 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ri_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "24398",
                    "1.11 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ri_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "28863",
                    "1.3 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ri_all-records_labels.zip", "49775", "2.45 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ri_all-records_labels.zip", "88662", "4.02 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ri_all-records_labels.zip", "44038", "1.51 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ri_all-records_labels.zip", "43611", "2.22 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ri_all-records_labels.zip", "33941", "1.8 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ri_all-records_labels.zip", "51710", "2.4 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ri_all-records_labels.zip", "64057", "2.81 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ri_all-records_labels.zip", "48785", "2.39 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ri_all-records_labels.zip", "55842", "2.75 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ri_all-records_labels.zip", "52960", "2.62 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ri_all-records_labels.zip", "61996", "3.04 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ri_originated-records_labels.zip",
                    "27005",
                    "1.25 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ri_originated-records_labels.zip",
                    "36923",
                    "1.65 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ri_originated-records_labels.zip",
                    "24598",
                    "766.74 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ri_originated-records_labels.zip",
                    "23923",
                    "1.13 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ri_originated-records_labels.zip",
                    "18005",
                    "891.11 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ri_originated-records_labels.zip",
                    "23931",
                    "1.07 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ri_originated-records_labels.zip",
                    "33549",
                    "1.38 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ri_originated-records_labels.zip",
                    "24337",
                    "1.11 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ri_originated-records_labels.zip",
                    "28439",
                    "1.3 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ri_originated-records_labels.zip",
                    "29485",
                    "1.37 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ri_originated-records_labels.zip",
                    "33911",
                    "1.55 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ri_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "22014",
                    "662.47 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ri_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "24278",
                    "740.23 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ri_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "19545",
                    "422.08 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ri_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "19238",
                    "594.54 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ri_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "14179",
                    "455.38 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ri_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "18140",
                    "535.59 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ri_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "29449",
                    "820.78 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ri_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "20369",
                    "581.77 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ri_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "24263",
                    "698.2 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ri_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "24398",
                    "725.42 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ri_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "28863",
                    "844.23 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ri_all-records_codes.zip", "49775", "1.57 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ri_all-records_codes.zip", "88662", "2.64 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ri_all-records_codes.zip", "44038", "997.28 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ri_all-records_codes.zip", "43611", "1.42 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ri_all-records_codes.zip", "33941", "1.14 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ri_all-records_codes.zip", "51710", "1.58 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ri_all-records_codes.zip", "64057", "1.89 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ri_all-records_codes.zip", "48785", "1.49 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ri_all-records_codes.zip", "55842", "1.73 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ri_all-records_codes.zip", "52960", "1.66 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ri_all-records_codes.zip", "61996", "1.93 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ri_originated-records_codes.zip",
                    "27005",
                    "818.97 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ri_originated-records_codes.zip",
                    "36923",
                    "1.12 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ri_originated-records_codes.zip",
                    "24598",
                    "532.25 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ri_originated-records_codes.zip",
                    "23923",
                    "744.4 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ri_originated-records_codes.zip",
                    "18005",
                    "586.22 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ri_originated-records_codes.zip",
                    "23931",
                    "716.77 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ri_originated-records_codes.zip",
                    "33549",
                    "938.52 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ri_originated-records_codes.zip",
                    "24337",
                    "705.92 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ri_originated-records_codes.zip",
                    "28439",
                    "835.63 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ri_originated-records_codes.zip",
                    "29485",
                    "889.58 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ri_originated-records_codes.zip",
                    "33911",
                    "1.01 MB",
                ),
            },
        },
    },
    "ks": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ks_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "57549",
                    "2.68 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ks_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "62611",
                    "2.93 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ks_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "50202",
                    "1.64 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ks_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "52685",
                    "2.73 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ks_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "43216",
                    "2.18 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ks_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "56265",
                    "2.59 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ks_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "78703",
                    "3.32 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ks_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "56542",
                    "2.6 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ks_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "67768",
                    "3.07 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ks_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "62047",
                    "2.98 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ks_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "73455",
                    "3.41 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ks_all-records_labels.zip", "124922", "6.39 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ks_all-records_labels.zip", "194856", "9.65 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ks_all-records_labels.zip", "107563", "3.99 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ks_all-records_labels.zip", "113367", "6.35 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ks_all-records_labels.zip", "96245", "5.33 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ks_all-records_labels.zip", "146968", "7.27 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ks_all-records_labels.zip", "175095", "8.11 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ks_all-records_labels.zip", "126214", "6.44 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ks_all-records_labels.zip", "149351", "7.61 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ks_all-records_labels.zip", "134547", "7.17 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ks_all-records_labels.zip", "149627", "7.77 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ks_originated-records_labels.zip",
                    "69335",
                    "3.31 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ks_originated-records_labels.zip",
                    "86578",
                    "4.16 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ks_originated-records_labels.zip",
                    "61197",
                    "2.05 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ks_originated-records_labels.zip",
                    "63448",
                    "3.34 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ks_originated-records_labels.zip",
                    "53984",
                    "2.79 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ks_originated-records_labels.zip",
                    "72280",
                    "3.42 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ks_originated-records_labels.zip",
                    "90077",
                    "3.93 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ks_originated-records_labels.zip",
                    "66876",
                    "3.14 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ks_originated-records_labels.zip",
                    "78256",
                    "3.64 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ks_originated-records_labels.zip",
                    "74582",
                    "3.64 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ks_originated-records_labels.zip",
                    "84924",
                    "4.01 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ks_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "57549",
                    "1.78 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ks_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "62611",
                    "2.02 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ks_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "50202",
                    "1.17 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ks_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "52685",
                    "1.86 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ks_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "43216",
                    "1.46 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ks_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "56265",
                    "1.79 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ks_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "78703",
                    "2.28 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ks_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "56542",
                    "1.71 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ks_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "67768",
                    "2.02 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ks_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "62047",
                    "1.98 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ks_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "73455",
                    "2.25 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ks_all-records_codes.zip", "124922", "4.16 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ks_all-records_codes.zip", "194856", "6.5 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ks_all-records_codes.zip", "107563", "2.69 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ks_all-records_codes.zip", "113367", "4.18 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ks_all-records_codes.zip", "96245", "3.49 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ks_all-records_codes.zip", "146968", "4.88 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ks_all-records_codes.zip", "175095", "5.5 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ks_all-records_codes.zip", "126214", "4.14 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ks_all-records_codes.zip", "149351", "4.91 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ks_all-records_codes.zip", "134547", "4.67 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ks_all-records_codes.zip", "149627", "5.06 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ks_originated-records_codes.zip",
                    "69335",
                    "2.18 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ks_originated-records_codes.zip",
                    "86578",
                    "2.85 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ks_originated-records_codes.zip",
                    "61197",
                    "1.44 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ks_originated-records_codes.zip",
                    "63448",
                    "2.26 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ks_originated-records_codes.zip",
                    "53984",
                    "1.86 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ks_originated-records_codes.zip",
                    "72280",
                    "2.34 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ks_originated-records_codes.zip",
                    "90077",
                    "2.69 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ks_originated-records_codes.zip",
                    "66876",
                    "2.05 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ks_originated-records_codes.zip",
                    "78256",
                    "2.38 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ks_originated-records_codes.zip",
                    "74582",
                    "2.39 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ks_originated-records_codes.zip",
                    "84924",
                    "2.62 MB",
                ),
            },
        },
    },
    "mt": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "21366",
                    "875.05 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "20722",
                    "828.42 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "18983",
                    "556.44 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "19758",
                    "888.25 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15841",
                    "699.12 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "19303",
                    "733.23 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "30035",
                    "1.08 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "18104",
                    "695.47 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "21854",
                    "845.34 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "23631",
                    "959.77 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mt_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "25225",
                    "1 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mt_all-records_labels.zip", "50537", "2.27 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mt_all-records_labels.zip", "72952", "3 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mt_all-records_labels.zip", "45597", "1.44 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mt_all-records_labels.zip", "46419", "2.32 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mt_all-records_labels.zip", "38476", "1.85 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mt_all-records_labels.zip", "55795", "2.26 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mt_all-records_labels.zip", "72632", "2.81 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mt_all-records_labels.zip", "45730", "1.97 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mt_all-records_labels.zip", "54464", "2.34 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mt_all-records_labels.zip", "56588", "2.52 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mt_all-records_labels.zip", "57320", "2.52 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mt_originated-records_labels.zip",
                    "26863",
                    "1.12 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mt_originated-records_labels.zip",
                    "31811",
                    "1.27 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mt_originated-records_labels.zip",
                    "24577",
                    "727.45 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mt_originated-records_labels.zip",
                    "25376",
                    "1.17 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mt_originated-records_labels.zip",
                    "21159",
                    "958.54 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mt_originated-records_labels.zip",
                    "26278",
                    "1.02 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mt_originated-records_labels.zip",
                    "36202",
                    "1.33 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mt_originated-records_labels.zip",
                    "23529",
                    "929.24 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mt_originated-records_labels.zip",
                    "27263",
                    "1.08 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mt_originated-records_labels.zip",
                    "31007",
                    "1.28 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mt_originated-records_labels.zip",
                    "31452",
                    "1.28 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "21366",
                    "564.56 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "20722",
                    "538.06 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "18983",
                    "389.92 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "19758",
                    "575.24 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15841",
                    "453.36 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "19303",
                    "479.86 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "30035",
                    "726.19 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "18104",
                    "448.42 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "21854",
                    "543.67 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "23631",
                    "616.38 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mt_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "25225",
                    "642.31 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mt_all-records_codes.zip", "50537", "1.41 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mt_all-records_codes.zip", "72952", "1.92 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mt_all-records_codes.zip", "45597", "947.96 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mt_all-records_codes.zip", "46419", "1.45 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mt_all-records_codes.zip", "38476", "1.16 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mt_all-records_codes.zip", "55795", "1.44 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mt_all-records_codes.zip", "72632", "1.84 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mt_all-records_codes.zip", "45730", "1.22 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mt_all-records_codes.zip", "54464", "1.45 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mt_all-records_codes.zip", "56588", "1.56 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mt_all-records_codes.zip", "57320", "1.57 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_mt_originated-records_codes.zip",
                    "26863",
                    "722 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_mt_originated-records_codes.zip",
                    "31811",
                    "828.36 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_mt_originated-records_codes.zip",
                    "24577",
                    "501.64 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_mt_originated-records_codes.zip",
                    "25376",
                    "750.19 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_mt_originated-records_codes.zip",
                    "21159",
                    "615.26 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_mt_originated-records_codes.zip",
                    "26278",
                    "663.11 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_mt_originated-records_codes.zip",
                    "36202",
                    "887.48 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_mt_originated-records_codes.zip",
                    "23529",
                    "592.46 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_mt_originated-records_codes.zip",
                    "27263",
                    "689.27 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_mt_originated-records_codes.zip",
                    "31007",
                    "815.5 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_mt_originated-records_codes.zip",
                    "31452",
                    "815.03 KB",
                ),
            },
        },
    },
    "ms": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ms_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "37426",
                    "1.74 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ms_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "50509",
                    "2.25 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ms_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "36762",
                    "1.08 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ms_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "33087",
                    "1.71 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ms_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "29718",
                    "1.39 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ms_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "41719",
                    "1.93 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ms_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "46880",
                    "1.96 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ms_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "34477",
                    "1.51 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ms_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "39727",
                    "1.77 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ms_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "40639",
                    "1.88 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ms_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "43832",
                    "1.98 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ms_all-records_labels.zip", "107199", "5.36 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ms_all-records_labels.zip", "173130", "7.83 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ms_all-records_labels.zip", "101384", "3.15 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ms_all-records_labels.zip", "95532", "5.35 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ms_all-records_labels.zip", "89193", "4.45 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ms_all-records_labels.zip", "136596", "6.41 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ms_all-records_labels.zip", "137988", "6 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ms_all-records_labels.zip", "106833", "5.1 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ms_all-records_labels.zip", "120079", "5.8 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ms_all-records_labels.zip", "115511", "5.75 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ms_all-records_labels.zip", "119816", "5.82 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ms_originated-records_labels.zip",
                    "51684",
                    "2.47 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ms_originated-records_labels.zip",
                    "75757",
                    "3.36 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ms_originated-records_labels.zip",
                    "51038",
                    "1.5 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ms_originated-records_labels.zip",
                    "47435",
                    "2.5 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ms_originated-records_labels.zip",
                    "44303",
                    "2.12 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ms_originated-records_labels.zip",
                    "63435",
                    "2.92 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ms_originated-records_labels.zip",
                    "64926",
                    "2.75 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ms_originated-records_labels.zip",
                    "49962",
                    "2.26 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ms_originated-records_labels.zip",
                    "55509",
                    "2.53 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ms_originated-records_labels.zip",
                    "57688",
                    "2.73 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ms_originated-records_labels.zip",
                    "59972",
                    "2.76 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ms_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "37426",
                    "1.15 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ms_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "50509",
                    "1.5 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ms_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "36762",
                    "770.12 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ms_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "33087",
                    "1.14 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ms_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "29718",
                    "914.92 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ms_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "41719",
                    "1.3 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ms_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "46880",
                    "1.32 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ms_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "34477",
                    "986.29 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ms_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "39727",
                    "1.16 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ms_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "40639",
                    "1.23 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ms_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "43832",
                    "1.29 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ms_all-records_codes.zip", "107199", "3.37 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ms_all-records_codes.zip", "173130", "5.1 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ms_all-records_codes.zip", "101384", "2.07 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ms_all-records_codes.zip", "95532", "3.43 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ms_all-records_codes.zip", "89193", "2.8 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ms_all-records_codes.zip", "136596", "4.22 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ms_all-records_codes.zip", "137988", "3.96 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ms_all-records_codes.zip", "106833", "3.19 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ms_all-records_codes.zip", "120079", "3.65 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ms_all-records_codes.zip", "115511", "3.61 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ms_all-records_codes.zip", "119816", "3.68 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ms_originated-records_codes.zip",
                    "51684",
                    "1.61 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ms_originated-records_codes.zip",
                    "75757",
                    "2.24 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ms_originated-records_codes.zip",
                    "51038",
                    "1.05 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ms_originated-records_codes.zip",
                    "47435",
                    "1.65 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ms_originated-records_codes.zip",
                    "44303",
                    "1.37 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ms_originated-records_codes.zip",
                    "63435",
                    "1.96 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ms_originated-records_codes.zip",
                    "64926",
                    "1.84 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ms_originated-records_codes.zip",
                    "49962",
                    "1.46 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ms_originated-records_codes.zip",
                    "55509",
                    "1.64 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ms_originated-records_codes.zip",
                    "57688",
                    "1.76 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ms_originated-records_codes.zip",
                    "59972",
                    "1.79 MB",
                ),
            },
        },
    },
    "sc": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "108076",
                    "5.05 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "106873",
                    "4.81 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "100333",
                    "3.01 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "92167",
                    "5.02 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "73174",
                    "3.73 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "86677",
                    "3.98 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "110931",
                    "4.77 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "78145",
                    "3.46 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "85858",
                    "3.92 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "100643",
                    "4.76 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sc_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "106107",
                    "5 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sc_all-records_labels.zip", "257644", "13.17 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sc_all-records_labels.zip", "383001", "17.86 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sc_all-records_labels.zip", "242772", "8.25 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sc_all-records_labels.zip", "225542", "13.41 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sc_all-records_labels.zip", "191197", "10.66 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sc_all-records_labels.zip", "271908", "13.26 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sc_all-records_labels.zip", "291014", "13.32 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sc_all-records_labels.zip", "218369", "11.01 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sc_all-records_labels.zip", "235957", "12.07 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sc_all-records_labels.zip", "259782", "13.73 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sc_all-records_labels.zip", "267040", "14.05 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sc_originated-records_labels.zip",
                    "131134",
                    "6.36 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sc_originated-records_labels.zip",
                    "161777",
                    "7.5 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sc_originated-records_labels.zip",
                    "123971",
                    "3.87 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sc_originated-records_labels.zip",
                    "114336",
                    "6.37 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sc_originated-records_labels.zip",
                    "93412",
                    "4.86 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sc_originated-records_labels.zip",
                    "118458",
                    "5.61 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sc_originated-records_labels.zip",
                    "133057",
                    "5.91 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sc_originated-records_labels.zip",
                    "97461",
                    "4.61 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sc_originated-records_labels.zip",
                    "105626",
                    "4.87 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sc_originated-records_labels.zip",
                    "127479",
                    "6.16 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sc_originated-records_labels.zip",
                    "130453",
                    "6.21 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "108076",
                    "3.37 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "106873",
                    "3.2 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "100333",
                    "2.11 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "92167",
                    "3.46 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "73174",
                    "2.49 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "86677",
                    "2.67 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "110931",
                    "3.27 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "78145",
                    "2.24 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "85858",
                    "2.58 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "100643",
                    "3.16 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sc_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "106107",
                    "3.31 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sc_all-records_codes.zip", "257644", "8.51 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sc_all-records_codes.zip", "383001", "11.71 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sc_all-records_codes.zip", "242772", "5.31 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sc_all-records_codes.zip", "225542", "8.88 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sc_all-records_codes.zip", "191197", "6.91 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sc_all-records_codes.zip", "271908", "8.77 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sc_all-records_codes.zip", "291014", "8.92 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sc_all-records_codes.zip", "218369", "6.92 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sc_all-records_codes.zip", "235957", "7.67 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sc_all-records_codes.zip", "259782", "8.91 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sc_all-records_codes.zip", "267040", "9.12 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sc_originated-records_codes.zip",
                    "131134",
                    "4.24 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sc_originated-records_codes.zip",
                    "161777",
                    "5.03 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sc_originated-records_codes.zip",
                    "123971",
                    "2.67 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sc_originated-records_codes.zip",
                    "114336",
                    "4.36 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sc_originated-records_codes.zip",
                    "93412",
                    "3.22 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sc_originated-records_codes.zip",
                    "118458",
                    "3.78 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sc_originated-records_codes.zip",
                    "133057",
                    "4.05 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sc_originated-records_codes.zip",
                    "97461",
                    "2.99 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sc_originated-records_codes.zip",
                    "105626",
                    "3.17 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sc_originated-records_codes.zip",
                    "127479",
                    "4.06 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sc_originated-records_codes.zip",
                    "130453",
                    "4.07 MB",
                ),
            },
        },
    },
    "ky": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ky_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "81819",
                    "3.99 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ky_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "82043",
                    "3.84 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ky_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "72775",
                    "2.34 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ky_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "71716",
                    "3.98 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ky_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "59329",
                    "3.1 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ky_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "73163",
                    "3.45 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ky_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "103950",
                    "4.54 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ky_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "80580",
                    "3.74 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ky_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "91441",
                    "4.28 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ky_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "89932",
                    "4.39 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ky_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "105634",
                    "5.06 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ky_all-records_labels.zip", "185587", "10.06 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ky_all-records_labels.zip", "285560", "14.05 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ky_all-records_labels.zip", "173004", "6.52 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ky_all-records_labels.zip", "167714", "10.04 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ky_all-records_labels.zip", "149317", "8.6 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ky_all-records_labels.zip", "215096", "10.84 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ky_all-records_labels.zip", "246427", "11.78 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ky_all-records_labels.zip", "203934", "10.77 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ky_all-records_labels.zip", "222486", "11.61 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ky_all-records_labels.zip", "215281", "11.75 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ky_all-records_labels.zip", "239015", "12.85 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ky_originated-records_labels.zip",
                    "100105",
                    "5.04 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ky_originated-records_labels.zip",
                    "121278",
                    "5.84 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ky_originated-records_labels.zip",
                    "91096",
                    "3.01 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ky_originated-records_labels.zip",
                    "88714",
                    "5.02 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ky_originated-records_labels.zip",
                    "76520",
                    "4.06 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ky_originated-records_labels.zip",
                    "99394",
                    "4.77 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ky_originated-records_labels.zip",
                    "123485",
                    "5.57 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ky_originated-records_labels.zip",
                    "98794",
                    "4.7 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ky_originated-records_labels.zip",
                    "109716",
                    "5.22 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ky_originated-records_labels.zip",
                    "110912",
                    "5.58 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ky_originated-records_labels.zip",
                    "125050",
                    "6.13 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ky_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "81819",
                    "2.64 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ky_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "82043",
                    "2.59 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ky_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "72775",
                    "1.68 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ky_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "71716",
                    "2.68 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ky_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "59329",
                    "2.06 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ky_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "73163",
                    "2.34 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ky_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "103950",
                    "3.13 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ky_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "80580",
                    "2.43 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ky_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "91441",
                    "2.81 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ky_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "89932",
                    "2.91 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ky_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "105634",
                    "3.33 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ky_all-records_codes.zip", "185587", "6.56 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ky_all-records_codes.zip", "285560", "9.35 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ky_all-records_codes.zip", "173004", "4.32 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ky_all-records_codes.zip", "167714", "6.5 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ky_all-records_codes.zip", "149317", "5.56 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ky_all-records_codes.zip", "215096", "7.24 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ky_all-records_codes.zip", "246427", "7.96 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ky_all-records_codes.zip", "203934", "6.87 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ky_all-records_codes.zip", "222486", "7.44 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ky_all-records_codes.zip", "215281", "7.63 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ky_all-records_codes.zip", "239015", "8.34 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_ky_originated-records_codes.zip",
                    "100105",
                    "3.34 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_ky_originated-records_codes.zip",
                    "121278",
                    "3.97 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_ky_originated-records_codes.zip",
                    "91096",
                    "2.12 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_ky_originated-records_codes.zip",
                    "88714",
                    "3.36 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_ky_originated-records_codes.zip",
                    "76520",
                    "2.67 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_ky_originated-records_codes.zip",
                    "99394",
                    "3.22 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_ky_originated-records_codes.zip",
                    "123485",
                    "3.84 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_ky_originated-records_codes.zip",
                    "98794",
                    "3.04 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_ky_originated-records_codes.zip",
                    "109716",
                    "3.39 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_ky_originated-records_codes.zip",
                    "110912",
                    "3.68 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_ky_originated-records_codes.zip",
                    "125050",
                    "4.01 MB",
                ),
            },
        },
    },
    "or": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_or_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "114167",
                    "5.46 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_or_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "101187",
                    "4.59 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_or_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "95129",
                    "2.88 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_or_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "97022",
                    "5.17 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_or_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "69787",
                    "3.39 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_or_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "77187",
                    "3.56 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_or_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "118063",
                    "5.04 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_or_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "80824",
                    "3.93 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_or_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "102166",
                    "4.84 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_or_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "102103",
                    "4.92 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_or_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "119486",
                    "5.65 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_or_all-records_labels.zip", "249739", "12.75 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_or_all-records_labels.zip", "376732", "17.18 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_or_all-records_labels.zip", "211344", "7.17 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_or_all-records_labels.zip", "214365", "12.36 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_or_all-records_labels.zip", "168582", "8.75 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_or_all-records_labels.zip", "251125", "12 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_or_all-records_labels.zip", "300552", "13.38 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_or_all-records_labels.zip", "204085", "10.92 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_or_all-records_labels.zip", "244799", "12.74 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_or_all-records_labels.zip", "240614", "12.69 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_or_all-records_labels.zip", "269285", "14.02 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_or_originated-records_labels.zip",
                    "136083",
                    "6.58 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_or_originated-records_labels.zip",
                    "151933",
                    "7.06 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_or_originated-records_labels.zip",
                    "116700",
                    "3.65 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_or_originated-records_labels.zip",
                    "117674",
                    "6.39 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_or_originated-records_labels.zip",
                    "87626",
                    "4.34 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_or_originated-records_labels.zip",
                    "97998",
                    "4.65 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_or_originated-records_labels.zip",
                    "134377",
                    "5.88 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_or_originated-records_labels.zip",
                    "98243",
                    "4.9 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_or_originated-records_labels.zip",
                    "118373",
                    "5.68 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_or_originated-records_labels.zip",
                    "128622",
                    "6.28 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_or_originated-records_labels.zip",
                    "144891",
                    "7.02 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_or_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "114167",
                    "3.73 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_or_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "101187",
                    "3.17 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_or_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "95129",
                    "1.97 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_or_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "97022",
                    "3.6 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_or_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "69787",
                    "2.33 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_or_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "77187",
                    "2.47 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_or_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "118063",
                    "3.58 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_or_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "80824",
                    "2.65 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_or_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "102166",
                    "3.28 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_or_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "102103",
                    "3.39 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_or_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "119486",
                    "3.83 MB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_or_all-records_codes.zip", "249739", "8.44 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_or_all-records_codes.zip", "376732", "11.64 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_or_all-records_codes.zip", "211344", "4.61 MB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_or_all-records_codes.zip", "214365", "8.29 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_or_all-records_codes.zip", "168582", "5.8 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_or_all-records_codes.zip", "251125", "8.16 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_or_all-records_codes.zip", "300552", "9.29 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_or_all-records_codes.zip", "204085", "7.17 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_or_all-records_codes.zip", "244799", "8.44 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_or_all-records_codes.zip", "240614", "8.5 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_or_all-records_codes.zip", "269285", "9.32 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_or_originated-records_codes.zip",
                    "136083",
                    "4.48 MB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_or_originated-records_codes.zip",
                    "151933",
                    "4.92 MB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_or_originated-records_codes.zip",
                    "116700",
                    "2.48 MB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_or_originated-records_codes.zip",
                    "117674",
                    "4.43 MB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_or_originated-records_codes.zip",
                    "87626",
                    "2.98 MB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_or_originated-records_codes.zip",
                    "97998",
                    "3.24 MB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_or_originated-records_codes.zip",
                    "134377",
                    "4.19 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_or_originated-records_codes.zip",
                    "98243",
                    "3.29 MB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_or_originated-records_codes.zip",
                    "118373",
                    "3.84 MB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_or_originated-records_codes.zip",
                    "128622",
                    "4.29 MB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_or_originated-records_codes.zip",
                    "144891",
                    "4.75 MB",
                ),
            },
        },
    },
    "sd": {
        "labels": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "17608",
                    "715.46 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15984",
                    "612.26 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15341",
                    "394.73 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "15835",
                    "706.73 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "12839",
                    "526.79 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "16258",
                    "623.5 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "24417",
                    "866.74 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "17828",
                    "666.34 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "20738",
                    "786.61 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "19523",
                    "775.49 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sd_first-lien-owner-occupied-1-4-family-records_labels.zip",
                    "24459",
                    "981.4 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sd_all-records_labels.zip", "37648", "1.67 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sd_all-records_labels.zip", "47432", "1.97 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sd_all-records_labels.zip", "33167", "980.45 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sd_all-records_labels.zip", "35072", "1.72 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sd_all-records_labels.zip", "29763", "1.37 MB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sd_all-records_labels.zip", "41213", "1.78 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sd_all-records_labels.zip", "53033", "2.13 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sd_all-records_labels.zip", "38426", "1.67 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sd_all-records_labels.zip", "45150", "1.96 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sd_all-records_labels.zip", "43401", "1.95 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sd_all-records_labels.zip", "48753", "2.2 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sd_originated-records_labels.zip",
                    "20937",
                    "887.21 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sd_originated-records_labels.zip",
                    "24091",
                    "970 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sd_originated-records_labels.zip",
                    "18871",
                    "517.46 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sd_originated-records_labels.zip",
                    "19418",
                    "890.97 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sd_originated-records_labels.zip",
                    "16136",
                    "696.36 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sd_originated-records_labels.zip",
                    "22824",
                    "912.18 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sd_originated-records_labels.zip",
                    "29867",
                    "1.11 MB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sd_originated-records_labels.zip",
                    "21818",
                    "862.15 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sd_originated-records_labels.zip",
                    "25068",
                    "980.72 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sd_originated-records_labels.zip",
                    "23684",
                    "969.63 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sd_originated-records_labels.zip",
                    "28651",
                    "1.18 MB",
                ),
            },
        },
        "codes": {
            "first-lien-owner-occupied-1-4-family-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "17608",
                    "452.93 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15984",
                    "392.92 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15341",
                    "275.01 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "15835",
                    "442.1 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "12839",
                    "334.62 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "16258",
                    "411.49 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "24417",
                    "586.34 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "17828",
                    "429.4 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "20738",
                    "504.37 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "19523",
                    "492.06 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sd_first-lien-owner-occupied-1-4-family-records_codes.zip",
                    "24459",
                    "623.71 KB",
                ),
            },
            "all-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sd_all-records_codes.zip", "37648", "1.02 MB"
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sd_all-records_codes.zip", "47432", "1.24 MB"
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sd_all-records_codes.zip", "33167", "657.41 KB"
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sd_all-records_codes.zip", "35072", "1.04 MB"
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sd_all-records_codes.zip", "29763", "835.84 KB"
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sd_all-records_codes.zip", "41213", "1.13 MB"
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sd_all-records_codes.zip", "53033", "1.39 MB"
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sd_all-records_codes.zip", "38426", "1.03 MB"
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sd_all-records_codes.zip", "45150", "1.22 MB"
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sd_all-records_codes.zip", "43401", "1.19 MB"
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sd_all-records_codes.zip", "48753", "1.35 MB"
                ),
            },
            "originated-records": {
                "2016": HmdaDataFile(
                    "hmda_2016_sd_originated-records_codes.zip",
                    "20937",
                    "557.49 KB",
                ),
                "2007": HmdaDataFile(
                    "hmda_2007_sd_originated-records_codes.zip",
                    "24091",
                    "623.6 KB",
                ),
                "2017": HmdaDataFile(
                    "hmda_2017_sd_originated-records_codes.zip",
                    "18871",
                    "357.8 KB",
                ),
                "2015": HmdaDataFile(
                    "hmda_2015_sd_originated-records_codes.zip",
                    "19418",
                    "553.25 KB",
                ),
                "2014": HmdaDataFile(
                    "hmda_2014_sd_originated-records_codes.zip",
                    "16136",
                    "436.32 KB",
                ),
                "2008": HmdaDataFile(
                    "hmda_2008_sd_originated-records_codes.zip",
                    "22824",
                    "595.53 KB",
                ),
                "2009": HmdaDataFile(
                    "hmda_2009_sd_originated-records_codes.zip",
                    "29867",
                    "746.74 KB",
                ),
                "2011": HmdaDataFile(
                    "hmda_2011_sd_originated-records_codes.zip",
                    "21818",
                    "549.43 KB",
                ),
                "2010": HmdaDataFile(
                    "hmda_2010_sd_originated-records_codes.zip",
                    "25068",
                    "623.74 KB",
                ),
                "2013": HmdaDataFile(
                    "hmda_2013_sd_originated-records_codes.zip",
                    "23684",
                    "608.21 KB",
                ),
                "2012": HmdaDataFile(
                    "hmda_2012_sd_originated-records_codes.zip",
                    "28651",
                    "744.18 KB",
                ),
            },
        },
    },
}
