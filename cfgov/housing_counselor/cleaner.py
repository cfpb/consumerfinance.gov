import re


REQUIRED_COUNSELOR_KEYS = {
    "adr1",
    "adr2",
    "agc_ADDR_LATITUDE",
    "agc_ADDR_LONGITUDE",
    "city",
    "email",
    "languages",
    "nme",
    "phone1",
    "services",
    "statecd",
    "weburl",
    "zipcd",
}


def clean_counselors(counselors):
    """Returns a cleaned set of HUD housing counselors."""
    return list(map(clean_counselor, counselors))


def clean_counselor(counselor):
    """Cleans a single housing counselor."""
    counselor = dict(counselor)

    if not REQUIRED_COUNSELOR_KEYS.issubset(set(counselor.keys())):
        raise ValueError("missing keys in counselor")

    lat_lng_keys = ("agc_ADDR_LATITUDE", "agc_ADDR_LONGITUDE")
    for key in lat_lng_keys:
        counselor[key] = float_or_none(counselor[key])

    for key in ("city", "nme"):
        counselor[key] = title_case(counselor[key])

    counselor["email"] = reformat_email(counselor["email"])
    counselor["weburl"] = reformat_weburl(counselor["weburl"])

    return counselor


def float_or_none(s):
    """Ensure a value is of type float if it is not none."""
    if s:
        return float(s)


def reformat_email(s):
    s = (s or "").strip()
    if "." in s and "@" in s:
        return s


def reformat_weburl(s):
    """Convert invalid URLs to null."""
    s = (s or "").strip()

    if s and "." in s and "notavailable" not in s:
        match = re.match(r"^http(s)?://", s)
        if not match:
            s = "http://" + s

        return s


def title_case(s):
    """Convert a string to have title case."""
    if not s:
        return None

    s = s.lower()
    parts = s.split(" ")
    lower_case = (
        "a",
        "an",
        "and",
        "as",
        "at",
        "by",
        "for",
        "in",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    )

    parts[0] = parts[0].title()
    parts = map(lambda part: part.title() if part not in lower_case else part, parts)

    return " ".join(parts)
