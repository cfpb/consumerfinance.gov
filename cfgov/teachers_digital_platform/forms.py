from .assessments import get_all_assessments


# Create named lists of forms from our assessments.
def get_form_lists():
    form_lists = {}
    for k, assessment in get_all_assessments().items():
        form_lists[k] = assessment.get_form_list(k)
    return form_lists

