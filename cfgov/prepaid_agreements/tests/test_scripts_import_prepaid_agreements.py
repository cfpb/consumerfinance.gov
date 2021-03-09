import unittest

from prepaid_agreements.scripts.import_prepaid_agreements_data import (
    import_agreements_data, import_products_data
)


class TestImports(unittest.TestCase):
    def test_import_data(self):
        data = {
            "agreements": [
                {
                    "agreement_id": "IFL-1",
                    "agreements_files_location": "Bank1_of_CFPB_200101.zip",
                    "created_date": "2020-01-01 12:34:56",
                    "effective_date": "01/01/2020",
                    "path": "CFPB Bank1/Bank1 of CFPB/20200101",
                    "product_id": "PRODUCT-1"
                },
                {
                    "agreement_id": "IFL-2",
                    "agreements_files_location": "Bank2_of_CFPB_20200202.zip",
                    "created_date": "2020-02-02 12:34:56",
                    "effective_date": "02/02/2020",
                    "path": "CFPB Bank2/Bank2_of_CFPB/20200202",
                    "product_id": "PRODUCT-2"
                },
                {
                    "agreement_id": "IFL-3",
                    "agreements_files_location": "Bank3_of_CFPB_20200303.zip",
                    "created_date": "2020-03-03 12:34:56",
                    "effective_date": "03/03/2020",
                    "path": "CFPB Bank3/Bank3_of CFPB/20200303",
                    "product_id": "PRODUCT-3"
                },
                {
                    "agreement_id": "IFL-4",
                    "agreements_files_location": "Bank4_of_CFPB_20200404.zip",
                    "created_date": "2020-04-04 12:34:56",
                    "effective_date": "04/04/2020",
                    "path": "CFPB Bank4/Bank4 of CFPB/20200404",
                    "product_id": "PRODUCT-4"
                },
                {
                    "agreement_id": "IFL-5",
                    "agreements_files_location": "Bank5_of_CFPB_20200505.zip",
                    "created_date": "2020-05-05 12:34:56",
                    "effective_date": "05/05/2020",
                    "path": "CFPB Bank5/Bank5_of_CFPB/20200505",
                    "product_id": "PRODUCT-5"
                },
                {
                    "agreement_id": "IFL-6",
                    "agreements_files_location": "Bank6_of_CFPB_20200606.zip",
                    "created_date": "2020-06-06 12:34:56",
                    "effective_date": "06/06/2020",
                    "path": "CFPB Bank6/Bank6_of CFPB/20200606",
                    "product_id": "PRODUCT-6"
                }
            ],
            "products": [
                {
                    "issuer_id": "1",
                    "issuer_name": "CFPB Bank1",
                    "other_relevant_parties": "Party",
                    "prepaid_type": "Payroll",
                    "product_id": "PRODUCT-1",
                    "product_name": "Bank1 of CFPB",
                    "program_manager": "CFPB",
                    "program_manager_exists": "Yes",
                    "status": "Active",
                    "withdrawal_date": "01/01/2020"
                },
                {
                    "issuer_id": "2",
                    "issuer_name": "CFPB Bank2",
                    "other_relevant_parties": "Party",
                    "prepaid_type": "Prison release",
                    "product_id": "PRODUCT-2",
                    "product_name": "Bank2_of_CFPB",
                    "program_manager": "CFPB",
                    "program_manager_exists": "Yes",
                    "status": "Active",
                    "withdrawal_date": "02/02/2020"
                },
                {
                    "issuer_id": "3",
                    "issuer_name": "CFPB Bank3",
                    "other_relevant_parties": "Party",
                    "prepaid_type": "Refunds",
                    "product_id": "PRODUCT-3",
                    "product_name": "Bank3 of CFPB",
                    "program_manager": "CFPB",
                    "program_manager_exists": "Yes",
                    "status": "Active",
                    "withdrawal_date": "03/03/2020"
                },
                {
                    "issuer_id": "4",
                    "issuer_name": "CFPB Bank4",
                    "other_relevant_parties": "Party",
                    "prepaid_type": "Student",
                    "product_id": "PRODUCT-4",
                    "product_name": "Bank4_of CFPB",
                    "program_manager": "CFPB",
                    "program_manager_exists": "Yes",
                    "status": "Active",
                    "withdrawal_date": "04/04/2020"
                },
                {
                    "issuer_id": "5",
                    "issuer_name": "CFPB Bank5",
                    "other_relevant_parties": "Party",
                    "prepaid_type": "Tax",
                    "product_id": "PRODUCT-5",
                    "product_name": "Bank5 of CFPB",
                    "program_manager": "CFPB",
                    "program_manager_exists": "Yes",
                    "status": "Active",
                    "withdrawal_date": "05/05/2020"
                },
                {
                    "issuer_id": "6",
                    "issuer_name": "CFPB Bank6",
                    "other_relevant_parties": "Party",
                    "prepaid_type": "Travel",
                    "product_id": "PRODUCT-6",
                    "product_name": "Bank6_of_CFPB",
                    "program_manager": "CFPB",
                    "program_manager_exists": "Yes",
                    "status": "Active",
                    "withdrawal_date": "06/06/2020"
                }
            ]
        }
        imported_products = import_products_data(data['products'])
        self.assertEqual(imported_products, ['1', '2', '3', '4', '5', '6'])

        imported_agreements = import_agreements_data(data['agreements'])
        self.assertEqual(imported_agreements, None)
