from __future__ import unicode_literals

import csv

from prepaid_agreements.models import PrepaidAgreement


def write_agreements_data():
    fieldnames = [
        'issuer_name', 'product_name', 'product_id', 'agreement_effective_date', 'created_date',
        'most_recent_agreement', 'withdrawal_date', 'current_status',
        'prepaid_product_type', 'program_manager_exists', 'program_manager',
        'other_relevant_parties', 'path', 'direct_download', 'agreement_id'
    ]
    # TODO: This needs to hook up to S3 bucket instead of writing locally. 
    with open('metadata.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        agreements = sorted(
            PrepaidAgreement.objects.all(),
            key=lambda agreement: (
                agreement.product.issuer_name,
                agreement.product.pk,
                agreement.product.name,
                agreement.created_date
            )
        )
        for agreement in agreements:
            product = agreement.product
            most_recent = 'Yes' if agreement.is_most_recent else 'No'
            other_relevant_parties = ''
            if product.other_relevant_parties:
                other_relevant_parties = product.other_relevant_parties.replace('\n', '; ')
            writer.writerow({
                'issuer_name': product.issuer_name,
                'product_name': product.name,
                'product_id': product.pk,
                'agreement_effective_date': agreement.effective_date,
                'created_date': agreement.created_date,
                'most_recent_agreement': most_recent,
                'withdrawal_date': product.withdrawal_date,
                'current_status': product.status,
                'prepaid_product_type': product.prepaid_type,
                'program_manager_exists': product.program_manager_exists,
                'program_manager': product.program_manager,
                'other_relevant_parties': other_relevant_parties,
                'path': agreement.bulk_download_path,
                'direct_download': agreement.compressed_files_url,
                'agreement_id': agreement.pk
            })


def run(*args):
    write_agreements_data()
