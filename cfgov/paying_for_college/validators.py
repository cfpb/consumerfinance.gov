ALLOWLIST_KEYS = {
    "alias": "string",
    "avgmonthlypay": "float",
    "avgstuloandebt": "integer",
    "avgstuloandebtrank": "integer",
    "badalias": "string",
    "bah": "integer",
    "books": "integer",
    "borrowingtotal": "integer",
    "city": "string",
    "control": "string",
    "defaultrate": "float",
    "family": "integer",
    "federaltotal": "integer",
    "firstyrcostattend": "integer",
    "firstyrnetcost": "integer",
    "gap": "integer",
    "gibill": "integer",
    "gibillbs": "integer",
    "gibillinstatetuition": "integer",
    "gibillla": "integer",
    "gibilltf": "integer",
    "gradplus": "integer",
    "gradplus_max": "integer",
    "gradplusgrad": "integer",
    "gradpluswithfee": "integer",
    "gradrate": "float",
    "gradraterank": "integer",
    "grantstotal": "integer",
    "homeequity": "integer",
    "homeequitygrad": "integer",
    "indicatorgroup": "integer",
    "instate": "boolean",
    "institutionalloan": "integer",
    "institutionalloan_max": "integer",
    "institutionalloangrad": "integer",
    "institutionalloanrate": "float",
    "kbyoss": "yes-no",
    "loandebt1yr": "integer",
    "loanlifetime": "integer",
    "loanmonthly": "integer",
    "loanmonthlyparent": "integer",
    "moneyforcollege": "integer",
    "netprice": "integer",
    "netprice110k": "integer",
    "netprice3ok": "integer",
    "netprice48k": "integer",
    "netprice75k": "integer",
    "netpricegeneral": "integer",
    "netpriceok": "integer",
    "offeraa": "yes-no",
    "offerba": "yes-no",
    "offergrad": "yes-no",
    "oncampusavail": "yes-no",
    "online": "yes-no",
    "otherexpenses": "integer",
    "otheroffcampus": "integer",
    "otheroncampus": "integer",
    "otherwfamily": "integer",
    "overborrowing": "integer",
    "parentplus": "integer",
    "parentplusgrad": "integer",
    "parentpluswithfee": "integer",
    "pell": "integer",
    "pell_max": "integer",
    "perkins": "integer",
    "perkins_max": "integer",
    "perkinsgrad": "integer",
    "personal": "integer",
    "prgmlength": "integer",
    "privateloan": "integer",
    "privateloan_max": "integer",
    "privateloangrad": "integer",
    "privateloanrate": "float",
    "privatetotal": "integer",
    "program": "string",
    "remainingcost": "integer",
    "repaymentterm": "integer",
    "retentrate": "float",
    "riskofdefault": "string",
    "roombrd": "integer",
    "roombrdoffcampus": "integer",
    "roombrdoncampus": "integer",
    "salaryexpected25yrs": "float",
    "salarymonthly": "float",
    "salaryneeded": "integer",
    "savings": "integer",
    "savingstotal": "integer",
    "scholar": "integer",
    "school": "string",
    "school_id": "integer",
    "staffsubsidized": "integer",
    "staffsubsidized_max": "integer",
    "staffsubsidizedgrad": "integer",
    "staffsubsidizedwithfee": "integer",
    "staffunsubsidized": "integer",
    "staffunsubsidized_max": "integer",
    "staffunsubsidizeddep_max": "integer",
    "staffunsubsidizedgrad": "integer",
    "staffunsubsidizedindep_max": "integer",
    "staffunsubsidizedwithfee": "integer",
    "state": "string",
    "state529plan": "integer",
    "tfinstate": "integer",
    "totaldebtgrad": "integer",
    "totalgrantsandsavings": "integer",
    "totaloutofpocket": "integer",
    "transportation": "integer",
    "tuitionassist": "integer",
    "tuitionassist_max": "integer",
    "tuitionfees": "integer",
    "tuitiongradindis": "integer",
    "tuitiongradins": "integer",
    "tuitiongradoss": "integer",
    "tuitionunderindis": "integer",
    "tuitionunderins": "integer",
    "tuitionundeross": "integer",
    "undergrad": "boolean",
    "unsubsidizedrate": "float",
    "workstudy": "integer",
    "yrincollege": "integer",
    "zip": "string",
}


def clean_integer(value):
    if value:
        try:
            checked = int(value)
        except Exception:
            return 0
        else:
            return checked
    else:
        return 0


def clean_float(value):
    if value:
        try:
            checked = float(value)
        except Exception:
            return 0
        else:
            return checked
    else:
        return 0


def clean_string(value):
    if value:
        try:
            checked = value.replace("<", "").replace(">", "")[:2000]
        except Exception:
            return ""
        else:
            return checked
    else:
        return ""


def clean_boolean(value):
    if hasattr(value, "lower") and value.lower() in ("false", "0"):
        return False
    if hasattr(value, "lower") and value.lower() in ("true", "1"):
        return True
    else:
        return ""


def clean_yes_no(value):
    if hasattr(value, "lower") and value.lower().strip() == "no":
        return "No"
    if hasattr(value, "lower") and value.lower().strip() == "yes":
        return "Yes"
    else:
        return ""
