from django.conf.urls import include, url


urlpatterns = [
    url(r'^understanding-your-financial-aid-offer/',
        include('college.disclosures.urls',
                namespace='disclosures')),
    # url(r'^repay-student-debt/$',
    #     BaseTemplateView.as_view(template_name='repay_student_debt.html'),
    #     name='pfc-repay'),
    # url(r'^explore-student-loan-options/$',
    #     BaseTemplateView.as_view(template_name='choose_a_loan.html'),
    #     name='pfc-choose'),
    # url(r'^choosing-college-bank-accounts/$',
    #     BaseTemplateView.as_view(template_name='manage_your_money.html'),
    #     name='pfc-manage'),
    # url(r'^know-before-you-owe-student-debt/$',
    #     BaseTemplateView.as_view(template_name='kbyo-static.html'),
    #     name='pfc-kbyo'),
    # url(r'^student-loan-forgiveness-pledge/$',
    #     BaseTemplateView.as_view(template_name='pledge-static.html'),
    #     name='pfc-pledge'),

]
