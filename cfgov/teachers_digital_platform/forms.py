from .assessments import assessments


# Create named lists of forms from our assessments.
form_lists = {}
for k, assessment in assessments.items():
    form_lists[k] = assessment.get_form_list(k)
