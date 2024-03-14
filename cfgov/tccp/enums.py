def make_choices(*choices):
    return [(choice, choice) for choice in choices]


BalanceComputationChoices = make_choices(
    "Average daily balance including new purchases",
    "Average daily balance excluding new purchases",
    "Adjusted balance",
    "Previous balance",
    "Other",
)


BalanceTransferFeeTypeChoices = make_choices(
    "1. If fee is charged in dollars, what is the amount?",
    "2. If fee is percentage of transaction amount, what is it?",
    "3. If there's a minimum dollar amount, what is it?",
    (
        "4. If the fee is not a percentage, or a percentage subject to a minimum "
        "dollar amount, how do you calculate the fee?"
    ),
)


CashAdvanceFeeTypeChoices = make_choices(
    "1. If the fee is charged in dollars, what is the amount?",
    "2. If the fee is a percentage of transaction amount, what is it?",
    "3. If there's a minimum dollar amount, what is it?",
    (
        "4. If the fee is not a percentage, or a percentage subject to a minimum "
        "dollar amount, how do you calculate the fee?"
    ),
)


ContactTypeChoices = make_choices("Phone", "Website")


CreditTierChoices = [
    ("No credit score", "I don’t have a credit score"),
    ("Credit score 619 or less", "Less than 619"),
    ("Credit scores from 620 to 719", "620-719"),
    ("Credit score of 720 or greater", "Greater than 720"),
]


CreditTierColumns = [
    ("Credit score 619 or less", "poor"),
    ("Credit scores from 620 to 719", "good"),
    ("Credit score of 720 or greater", "great"),
]


FeaturesChoices = make_choices(
    "Contactless Payments",
    "Chip card",
    "Fee-free foreign transactions",
    "Mobile wallet provisioning (for example, Apple Pay)",
    "Other",
)


ForeignTransactionFeeTypeChoices = make_choices(
    "1. If fee is charged in dollars, what is the amount?",
    "2. If fee is percentage of transaction amount, what is it?",
    "3. If there's a minimum dollar amount, what is it?",
    (
        "4. If the fee is not a percentage, or a percentage subject to a minimum "
        "dollar amount, how do you calculate the fee?"
    ),
)


GeoAvailabilityChoices = make_choices(
    "National",
    "Regional",
    "One State/Territory",
)


IndexChoices = make_choices(
    "Prime",
    "One-month T-bill",
    "Three-month T-bill",
    "Six-month T-bill",
    "One-year T-bill",
    "Fed Funds",
    "Cost of Funds",
    "Federal Reserve Discount Rate",
    "Other",
)


IndexTypeChoices = make_choices("F", "V")


LateFeeTypeChoices = make_choices(
    "1. What is the amount of the first late fee on the account?",
    (
        "2. What is the amount of late fees charged within six billing cycles of a "
        "previous late fee (repeat late fee)?"
    ),
    (
        "3. If you charge late fees that are not fixed dollar amounts, please explain "
        "your late fee policy here."
    ),
)


OverlimitFeeTypeChoices = make_choices(
    "1. What is the amount of the overlimit fee when charged?",
    (
        "2. If you charge overlimit fees that are not fixed dollar amounts, please "
        "explain what overlimit fees you charge here:"
    ),
)


PeriodicFeeTypeChoices = make_choices("Annual", "Monthly", "Weekly", "Other")


PurchaseTransactionFeeTypeChoices = make_choices(
    "1. If you have such a charge, enter the amount of the charge in dollars here:",
    (
        "2. or if the charge is a percentage of the transaction amount, enter that "
        "percentage here"
    ),
    "3. If there's a minimum dollar amount, what is it?",
    (
        "4. If the fee is not a percentage, or a percentage subject to a minimum "
        "dollar amount, how do you calculate the fee?"
    ),
)


RequirementsForOpeningChoices = make_choices(
    "Geographic Restrictions Beyond Place of Residence",
    "Professional Affiliation",
    "Other. Please Describe:",
)


RewardsChoices = make_choices(
    "Cashback rewards", "Travel-related rewards", "Other rewards"
)


ServicesChoices = make_choices(
    "Access to Free Credit Scores",
    "Automobile rental insurance",
    "Credit card registration",
    "Debt cancellation coverage",
    "Discounts on purchases of goods and services (non travel related)",
    "Extension on manufacturer’s warranty",
    "Other",
)


StateChoices = make_choices(
    "AA",
    "AE",
    "AK",
    "AL",
    "AP",
    "AR",
    "AS",
    "AZ",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "FM",
    "GA",
    "GU",
    "HI",
    "IA",
    "ID",
    "IL",
    "IN",
    "KS",
    "KY",
    "LA",
    "MA",
    "MD",
    "ME",
    "MH",
    "MI",
    "MN",
    "MO",
    "MP",
    "MS",
    "MT",
    "NC",
    "ND",
    "NE",
    "NH",
    "NJ",
    "NM",
    "NV",
    "NY",
    "OH",
    "OK",
    "OR",
    "PA",
    "PR",
    "PW",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VA",
    "VI",
    "VT",
    "WA",
    "WI",
    "WV",
    "WY",
)
