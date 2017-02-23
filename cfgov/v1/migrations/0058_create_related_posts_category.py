# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0057_rename_relate_posts_to_relate_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedPostsCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=255, choices=[(b'Blog', ((b'at-the-cfpb', b'At the CFPB'), (b'policy-compliance', b'Policy & Compliance'), (b'data-research-reports', b'Data, research & reports'), (b'info-for-consumers', b'Info for consumers'))), (b'Newsroom', ((b'op-ed', b'Op-Ed'), (b'press-release', b'Press Release'), (b'speech', b'Speech'), (b'testimony', b'Testimony')))])),
                ('page', modelcluster.fields.ParentalKey(related_name='related_posts_categories', to='v1.CFGOVPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='cfgovpagecategory',
            name='name',
            field=models.CharField(max_length=255, choices=[(b'Administration adjudication docket', ((b'administrative-adjudication', b'Administrative adjudication'), (b'stipulation-and-constent-order', b'Stipulation and consent order'))), (b'Amicus Brief', ((b'us-supreme-court', b'U.S. Supreme Court'), (b'fed-circuit-court', b'Federal Circuit Court'), (b'fed-district-court', b'Federal District Court'), (b'state-court', b'State Court'))), (b'Blog', ((b'at-the-cfpb', b'At the CFPB'), (b'policy-compliance', b'Policy & Compliance'), (b'data-research-reports', b'Data, research & reports'), (b'info-for-consumers', b'Info for consumers'))), (b'Enforcement Action', ((b'fed-district-case', b'Federal district court case'), (b'administrative-adjudication-2', b'Administrative adjudication'), (b'stipulation-and-consent-order-2', b'Stipulation and consent order'))), (b'Final Rule', ((b'interim-final-rule', b'Interim Final Rule'), (b'final-rule', b'Final Rule'))), (b'FOIA Frequently Requested Record', ((b'report', b'Report'), (b'log', b'Log'), (b'record', b'Record'))), (b'Implementation Resource', ((b'compliance-aid', b'Compliance aid'), (b'official-guidance', b'Official guidance'))), (b'Newsroom', ((b'op-ed', b'Op-Ed'), (b'press-release', b'Press Release'), (b'speech', b'Speech'), (b'testimony', b'Testimony'))), (b'Notice and Opportunity for Comment', ((b'notice-proposed-rule', b'Advanced Notice of Proposed Rulemaking'), (b'proposed-rule', b'Proposed Rule'), (b'interim-final-rule-2', b'Interim Final Rule'), (b'request-comment-info', b'Request for Comment or Information'), (b'proposed-policy', b'Proposed Policy'), (b'intent-preempt-determ', b'Intent to make Preemption Determination'), (b'info-collect-activity', b'Information Collection Activities'), (b'notice-privacy-act', b'Notice related to Privacy Act'))), (b'Research Report', ((b'consumer-complaint', b'Consumer Complaint'), (b'super-highlight', b'Supervisory Highlights'), (b'data-point', b'Data Point'), (b'industry-markets', b'Industry and markets'), (b'consumer-edu-empower', b'Consumer education and empowerment'), (b'to-congress', b'To Congress'))), (b'Rule under development', ((b'notice-proposed-rule-2', b'Advanced Notice of Proposed Rulemaking'), (b'proposed-rule-2', b'Proposed Rule'))), (b'Story', ((b'auto-loans', b'Auto loans'), (b'bank-accts-services', b'Bank accounts and services'), (b'credit-cards', b'Credit cards'), (b'credit-reports-scores', b'Credit reports and scores'), (b'debt-collection', b'Debt collection'), (b'money-transfers', b'Money transfers'), (b'mortgages', b'Mortgages'), (b'payday-loans', b'Payday loans'), (b'prepaid-cards', b'Prepaid cards'), (b'student-loans', b'Student loans')))]),
        ),
    ]
