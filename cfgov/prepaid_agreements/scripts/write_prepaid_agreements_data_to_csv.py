# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import csv

from prepaid_agreements.models import PrepaidAgreement


def write_agreements_data(path=''):
    agreements_fieldnames = [
        'issuer_name', 'product_name', 'product_id',
        'agreement_effective_date', 'agreement_id', 'most_recent_agreement',
        'created_date', 'current_status', 'withdrawal_date',
        'prepaid_product_type', 'program_manager_exists', 'program_manager',
        'other_relevant_parties', 'path', 'direct_download'
    ]
    products_fieldnames = [
        'issuer_name', 'product_name', 'product_id',
        'agreement_effective_date', 'agreement_id',
        'created_date', 'current_status', 'withdrawal_date',
        'prepaid_product_type', 'program_manager_exists', 'program_manager',
        'other_relevant_parties', 'path', 'direct_download'
    ]

    agreements_location = path + 'prepaid_metadata_all_agreements.csv'
    products_location = path + 'prepaid_metadata_recent_agreements.csv'
    agreements_file = open(agreements_location, 'w')
    products_file = open(products_location, 'w')

    agreements_writer = csv.DictWriter(
        agreements_file,
        fieldnames=agreements_fieldnames
    )
    agreements_writer.writeheader()

    products_writer = csv.DictWriter(
        products_file,
        fieldnames=products_fieldnames
    )
    products_writer.writeheader()

    agreements = sorted(
        PrepaidAgreement.objects.all(),
        key=lambda agreement: (
            agreement.product.issuer_name,
            agreement.product.name,
            agreement.product.pk,
            agreement.created_time
        )
    )

    for agreement in agreements:
        product = agreement.product
        most_recent = 'Yes' if agreement.is_most_recent else 'No'
        created_time = agreement.created_time.strftime('%Y-%m-%d %H:%M:%S')

        other_relevant_parties = product.other_relevant_parties
        if other_relevant_parties:
            other_relevant_parties = other_relevant_parties.replace(
                '\n', '; '
            ).encode('utf-8')
        else:
            other_relevant_parties = 'No information provided'

        program_manager = product.program_manager
        if program_manager:
            program_manager = program_manager.encode('utf-8')

        data = {
            'issuer_name': product.issuer_name.encode('utf-8'),
            'product_name': product.name.encode('utf-8'),
            'product_id': product.pk,
            'agreement_effective_date': agreement.effective_date,
            'created_date': created_time,
            'withdrawal_date': product.withdrawal_date,
            'current_status': product.status,
            'prepaid_product_type': product.prepaid_type,
            'program_manager_exists': product.program_manager_exists,
            'program_manager': program_manager,
            'other_relevant_parties': other_relevant_parties,
            'path': agreement.bulk_download_path,
            'direct_download': agreement.compressed_files_url,
            'agreement_id': agreement.pk
        }

        # Product-level CSV only includes data
        # for a product's most recent agreement,
        # such that there is one row per product ID
        if agreement.is_most_recent:
            products_writer.writerow(data)

        data['most_recent_agreement'] = most_recent
        agreements_writer.writerow(data)

    agreements_file.close()
    products_file.close()


def run(*args):
    if args:
        write_agreements_data(path=args[0])
    else:
        write_agreements_data()
