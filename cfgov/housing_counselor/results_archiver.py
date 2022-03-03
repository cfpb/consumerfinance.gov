import json
from zipfile import ZIP_DEFLATED, ZipFile

json_file_name = "HUD_approved_housing_counselors.json"


# By request from stakeholders in the Office of Innovation, save a
# list of the full results we receive from the HUD API, in case of
# future enforcement actions.

# As an MVP, we're saving the complete JSON response, zipped. As a
# future enhancement, we could consider improving the format of the
# data, e.g. as CSV.
def save_list(counselors, path):
    with ZipFile(path, "w", ZIP_DEFLATED, allowZip64=True) as zip_file:
        zip_file.writestr(json_file_name, json.dumps(counselors))
