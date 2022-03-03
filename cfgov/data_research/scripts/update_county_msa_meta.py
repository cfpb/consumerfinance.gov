import logging

from data_research.models import County, MetroArea, MortgageMetaData, State
from data_research.mortgage_utilities.fips_meta import (
    FIPS,
    NON_STATES,
    load_fips_meta,
)

logger = logging.getLogger(__name__)

NON_STATE_FIPS = NON_STATES.values()


def update_allowlist():
    county_list = [county.fips for county in County.objects.filter(valid=True)]
    msa_list = [msa.fips for msa in MetroArea.objects.filter(valid=True)]
    state_list = [
        state.fips for state in State.objects.exclude(fips__in=NON_STATE_FIPS)
    ]
    non_msa_list = [
        "{}-non".format(state.fips)
        for state in State.objects.filter(fips__in=state_list)
        if state.non_msa_valid is True
    ]
    final_list = (
        sorted(county_list)
        + sorted(msa_list)
        + sorted(state_list)
        + sorted(non_msa_list)
    )
    allowlist = MortgageMetaData.objects.get(name="allowlist")
    allowlist.json_value = final_list
    allowlist.save()


def update_state_to_geo_meta(geo):
    """
    Assemble dictionaries that map state abbreviations to all counties, metro
    areas and non-metro-areas in a given state, for use in building drop-downs.

    Areas are marked `valid: true` or `valid: false` based on whether they meet
    our display threshold of reporting at least 1,000 open mortgages.

    An MSA entry, delivering metadata for a state's MSA and non-MSA areas,
    will look like this:
    ```json
    {
        "HI": {
            "metros": [
                {
                    "fips": "27980",
                    "name": "Kahului-Wailuku-Lahaina, HI",
                    "valid": false
                },
                {
                    "fips": "46520",
                    "name": "Urban Honolulu, HI",
                    "valid": true
                },
                {
                    "fips": "15-non",
                    "valid": true,
                    "name": "Hawaii non-metro area"
                },
            "state_fips": "15",
            "state_name": "Hawaii"
        },
    ...
    }
    ```

    A county meta entry, showing all counties in a state, will look like this:
    ```json
    {
        "DE": {
            "counties": [
                {
                    "fips": "10001",
                    "name": "Kent County"
                    "valid": true,
                },
                {
                    "fips": "10003",
                    "name": "New Castle County"
                    "valid": true,
                },
                {
                    "fips": "10005",
                    "name": "Sussex County"
                    "valid": true,
                }
            ],
            "state_fips": "10",
            "state_name": "Delaware"
        },
    ...
    }
    ```
    """
    non_msa_fips_output = []
    geo_dict = {
        "county": {
            "geo_list": "counties",
            "output_slug": "state_county_meta",
            "fips_dict": FIPS.county_fips,
        },
        "msa": {
            "geo_list": "metros",
            "output_slug": "state_msa_meta",
            "fips_dict": FIPS.msa_fips,
        },
    }
    g_dict = geo_dict[geo]
    fips_dict = g_dict["fips_dict"]
    geo_list = g_dict["geo_list"]
    setup = {
        FIPS.state_fips[fips]["abbr"]: {
            "state_fips": fips,
            "state_name": FIPS.state_fips[fips]["name"],
            geo_list: [],
        }
        for fips in FIPS.state_fips
        if fips not in NON_STATE_FIPS
    }
    for fips in fips_dict:
        _dict = fips_dict[fips]
        geo_name = _dict["name"]
        geo_valid = fips in FIPS.allowlist
        if geo == "msa":
            msa_state_list = []
            for county_fips in _dict["county_list"]:
                state = FIPS.county_fips[county_fips]["state"]
                if state not in msa_state_list:
                    msa_state_list.append(state)
            for state_abbr in msa_state_list:
                setup[state_abbr][geo_list].append(
                    {"name": geo_name, "fips": fips, "valid": geo_valid}
                )
        else:  # geo is 'county'
            this_state = FIPS.county_fips[fips]["state"]
            setup[this_state][geo_list].append(
                {"name": geo_name, "fips": fips, "valid": geo_valid}
            )
        for state_abbr in setup:
            setup[state_abbr][geo_list].sort(key=lambda entry: entry["fips"])
    if geo == "msa":
        live_fips = [
            fips for fips in FIPS.state_fips if fips not in NON_STATE_FIPS
        ]
        for state_fips in live_fips:
            non_fips = "{}-non".format(state_fips)
            s_dict = FIPS.state_fips[state_fips]
            state_abbr = s_dict["abbr"]
            state_name = s_dict["name"]
            non_fips_name = "Non-metro area of {}".format(state_name)
            non_valid = non_fips in FIPS.allowlist
            setup[state_abbr][geo_list].append(
                {
                    "fips": non_fips,
                    "valid": non_valid,
                    "name": "Non-metro area of {}".format(state_name),
                }
            )
            non_msa_fips_output.append(
                {
                    "fips": non_fips,
                    "valid": non_valid,
                    "name": non_fips_name,
                    "state_name": state_name,
                    "abbr": state_abbr,
                }
            )
    # save to database
    slug = geo_dict[geo]["output_slug"]
    meta_obj, cr = MortgageMetaData.objects.get_or_create(name=slug)
    meta_obj.json_value = setup
    meta_obj.save()
    logger.info("Saved metadata object '{}.'".format(slug))
    if non_msa_fips_output:
        non_msa_fips_output.sort(key=lambda k: k["state_name"])
        non_meta_obj, cr = MortgageMetaData.objects.get_or_create(
            name="non_msa_fips"
        )
        non_meta_obj.json_value = non_msa_fips_output
        non_meta_obj.save()
        logger.info("Saved non_msa_fips")


def run():
    update_allowlist()
    load_fips_meta()
    for geo in ["msa", "county"]:
        update_state_to_geo_meta(geo)
