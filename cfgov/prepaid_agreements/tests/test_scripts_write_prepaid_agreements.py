from datetime import date, datetime, timedelta
from unittest import mock

from django.test import TestCase
from django.utils.timezone import make_aware

from prepaid_agreements.models import PrepaidAgreement, PrepaidProduct
from prepaid_agreements.scripts.write_prepaid_agreements_data_to_csv import (
    write_agreements_data,
)

S3_PATH = "https://files.consumerfinance.gov/a/assets/prepaid-agreements/"


class TestViews(TestCase):
    def setUp(self):
        self.issuer_name1 = "Bank of CFPB"
        self.issuer_name2 = "CFPB Bank"
        self.issuer_name3 = "Bank_of CFPB"

        self.product_name1 = self.issuer_name2
        self.product_name2 = self.issuer_name1
        self.product_name3 = self.issuer_name2.replace(" ", "_")

        self.product1 = PrepaidProduct(
            name=self.product_name1,
            issuer_name=self.issuer_name1,
            prepaid_type="Tax",
        )
        self.product1.save()
        self.product2 = PrepaidProduct(
            name=self.product_name2,
            issuer_name=self.issuer_name2,
            prepaid_type="Tax",
            other_relevant_parties="Party",
        )
        self.product2.save()
        self.product3 = PrepaidProduct(
            name=self.product_name3,
            issuer_name=self.issuer_name3,
            prepaid_type="Tax",
            other_relevant_parties="Party",
        )
        self.product3.save()

        effective_date = date(month=2, day=3, year=2019)
        created_date = make_aware(datetime(month=4, day=1, year=2020))
        filename1 = self.product_name1.replace(" ", "_") + "_01_04_2020.zip"
        filename2 = self.product_name2.replace(" ", "_") + "_02_04_2020.zip"
        filename3 = self.product_name3.replace(" ", "_") + "_03_04_2020.zip"
        self.path1 = self.issuer_name1 + "/" + self.product_name1 + "/20200401"
        self.path2 = self.issuer_name2 + "/" + self.product_name2 + "/20200402"
        self.path3 = self.issuer_name3 + "/" + self.product_name3 + "/20200403"
        self.direct_download1 = S3_PATH + filename1
        self.direct_download2 = S3_PATH + filename2
        self.direct_download3 = S3_PATH + filename3

        self.agreement_old = PrepaidAgreement(
            compressed_files_url=self.direct_download1,
            bulk_download_path=self.path1,
            filename=filename1,
            effective_date=effective_date,
            created_time=created_date - timedelta(hours=1),
            product=self.product1,
        )
        self.agreement_old.save()
        self.agreement_older = PrepaidAgreement(
            compressed_files_url=self.direct_download2,
            bulk_download_path=self.path2,
            filename=filename2,
            effective_date=effective_date,
            created_time=created_date - timedelta(hours=2),
            product=self.product2,
        )
        self.agreement_older.save()
        self.agreement_new = PrepaidAgreement(
            compressed_files_url=self.direct_download1,
            bulk_download_path=self.path1,
            filename=filename1,
            effective_date=effective_date,
            created_time=created_date,
            product=self.product1,
        )
        self.agreement_new.save()
        self.agreement_newer = PrepaidAgreement(
            compressed_files_url=self.direct_download3,
            bulk_download_path=self.path3,
            filename=filename3,
            effective_date=effective_date,
            created_time=created_date + timedelta(hours=1),
            product=self.product3,
        )
        self.agreement_newer.save()

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_write_agreements_data(self, mock_open):
        # Run the write function
        write_agreements_data()

        mock_file_handle = mock_open()

        # Make sure each file's headers exist
        mock_file_handle.write.assert_any_call(
            "issuer_name,product_name,product_id,"
            "agreement_effective_date,agreement_id,most_recent_agreement,"
            "created_date,current_status,withdrawal_date,"
            "prepaid_product_type,program_manager_exists,program_manager,"
            "other_relevant_parties,path,direct_download\r\n"
        )
        mock_file_handle.write.assert_any_call(
            "issuer_name,product_name,product_id,"
            "agreement_effective_date,agreement_id,"
            "created_date,current_status,withdrawal_date,"
            "prepaid_product_type,program_manager_exists,program_manager,"
            "other_relevant_parties,path,direct_download\r\n"
        )

        # Make sure expected data rows exist
        mock_file_handle.write.assert_any_call(
            self.issuer_name1
            + ","
            + self.product_name1
            + ","
            + str(self.product1.pk)
            + ",2019-02-03,"
            + str(self.agreement_old.pk)
            + ",No,2020-04-01 03:00:00,,,Tax,,,"
            "No information provided,"
            + self.path1
            + ","
            + self.direct_download1
            + "\r\n"
        )
        mock_file_handle.write.assert_any_call(
            self.issuer_name1
            + ","
            + self.product_name1
            + ","
            + str(self.product1.pk)
            + ",2019-02-03,"
            + str(self.agreement_new.pk)
            + ",2020-04-01 04:00:00,,,Tax,,,"
            "No information provided,"
            + self.path1
            + ","
            + self.direct_download1
            + "\r\n"
        )
        mock_file_handle.write.assert_any_call(
            self.issuer_name1
            + ","
            + self.product_name1
            + ","
            + str(self.product1.pk)
            + ",2019-02-03,"
            + str(self.agreement_new.pk)
            + ",Yes,2020-04-01 04:00:00,,,Tax,,,"
            "No information provided,"
            + self.path1
            + ","
            + self.direct_download1
            + "\r\n"
        )
        mock_file_handle.write.assert_any_call(
            self.issuer_name2
            + ","
            + self.product_name2
            + ","
            + str(self.product2.pk)
            + ",2019-02-03,"
            + str(self.agreement_older.pk)
            + ",2020-04-01 02:00:00,,,Tax,,,Party,"
            + self.path2
            + ","
            + self.direct_download2
            + "\r\n"
        )
        mock_file_handle.write.assert_any_call(
            self.issuer_name2
            + ","
            + self.product_name2
            + ","
            + str(self.product2.pk)
            + ",2019-02-03,"
            + str(self.agreement_older.pk)
            + ",Yes,2020-04-01 02:00:00,,,Tax,,,Party,"
            + self.path2
            + ","
            + self.direct_download2
            + "\r\n"
        )
        mock_file_handle.write.assert_any_call(
            self.issuer_name3
            + ","
            + self.product_name3
            + ","
            + str(self.product3.pk)
            + ",2019-02-03,"
            + str(self.agreement_newer.pk)
            + ",2020-04-01 05:00:00,,,Tax,,,Party,"
            + self.path3
            + ","
            + self.direct_download3
            + "\r\n"
        )
        mock_file_handle.write.assert_any_call(
            self.issuer_name3
            + ","
            + self.product_name3
            + ","
            + str(self.product3.pk)
            + ",2019-02-03,"
            + str(self.agreement_newer.pk)
            + ",Yes,2020-04-01 05:00:00,,,Tax,,,Party,"
            + self.path3
            + ","
            + self.direct_download3
            + "\r\n"
        )
