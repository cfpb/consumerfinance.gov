import requests

from filing_instruction_guide.data_point_models import DataFieldJson, DataPoint


def run(form_data, page):
    url = form_data["data_points_download_location"]
    if url:
        response = requests.get(url)
        data = response.json()

        if data:
            page.data_points.clear()
            for point in data["data_points"]:
                pt = DataPoint(
                    number=int(point["number"]),
                    title=point["title"],
                    anchor=point["anchor"],
                    rule_section=point["rule_section"],
                    intro_text=point["intro_text"],
                )

                for field in point["data_fields"]:
                    fj = DataFieldJson(info=field)
                    pt.data_fields_json.add(fj)

                page.data_points.add(pt)
