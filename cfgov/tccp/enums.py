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
        "4. If the fee is not a percentage, or a percentage subject to a "
        "minimum dollar amount, how do you calculate the fee?"
    ),
)


CashAdvanceFeeTypeChoices = make_choices(
    "1. If the fee is charged in dollars, what is the amount?",
    "2. If the fee is a percentage of transaction amount, what is it?",
    "3. If there's a minimum dollar amount, what is it?",
    (
        "4. If the fee is not a percentage, or a percentage subject to a "
        "minimum dollar amount, how do you calculate the fee?"
    ),
)


ContactTypeChoices = make_choices("Phone", "Website")


CreditTierChoices = [
    ("No credit score", "I don’t have a credit score"),
    ("Credit score 619 or less", "619 or less"),
    ("Credit scores from 620 to 719", "620-719"),
    ("Credit score of 720 or greater", "720 and greater"),
]


CreditTierConciseChoices = [
    ("No credit score", "No score"),
    ("Credit score 619 or less", "619 or less"),
    ("Credit scores from 620 to 719", "620-719"),
    ("Credit score of 720 or greater", "720+"),
]


CreditTierColumns = [
    ("Credit score 619 or less", "poor"),
    ("Credit scores from 620 to 719", "good"),
    ("Credit score of 720 or greater", "great"),
]


CreditTierConciseColumnChoices = [
    (value, concise_label, dict(CreditTierColumns).get(value))
    for value, concise_label in CreditTierConciseChoices
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
        "4. If the fee is not a percentage, or a percentage subject to a "
        "minimum dollar amount, how do you calculate the fee?"
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


InstitutionTypeChoices = make_choices("Bank", "CU")


LateFeeTypeChoices = make_choices(
    "1. What is the amount of the first late fee on the account?",
    (
        "2. What is the amount of late fees charged within six billing cycles "
        "of a previous late fee (repeat late fee)?"
    ),
    (
        "3. If you charge late fees that are not fixed dollar amounts, please "
        "explain your late fee policy here."
    ),
)


OverlimitFeeTypeChoices = make_choices(
    "1. What is the amount of the overlimit fee when charged?",
    (
        "2. If you charge overlimit fees that are not fixed dollar amounts, "
        "please explain what overlimit fees you charge here:"
    ),
)


PeriodicFeeTypeChoices = make_choices("Annual", "Monthly", "Weekly", "Other")


PurchaseAPRRatings = [
    (0, "less"),
    (1, "average"),
    (2, "more"),
]


PurchaseTransactionFeeTypeChoices = make_choices(
    (
        "1. If you have such a charge, enter the amount of the charge in "
        "dollars here:"
    ),
    (
        "2. or if the charge is a percentage of the transaction amount, enter "
        "that percentage here"
    ),
    "3. If there's a minimum dollar amount, what is it?",
    (
        "4. If the fee is not a percentage, or a percentage subject to a "
        "minimum dollar amount, how do you calculate the fee?"
    ),
)


RequirementsForOpeningChoices = make_choices(
    "Geographic Restrictions Beyond Place of Residence",
    "Professional Affiliation",
    "Other. Please Describe:",
)


RewardsChoices = [
    ("Cashback rewards", "Cash back"),
    ("Travel-related rewards", "Travel"),
    ("Other rewards", "Other"),
]


ServicesChoices = make_choices(
    "Access to Free Credit Scores",
    "Automobile rental insurance",
    "Credit card registration",
    "Debt cancellation coverage",
    "Discounts on purchases of goods and services (non travel related)",
    "Extension on manufacturer’s warranty",
    "Other",
)


StateChoices = [
    ("AL", "Alabama"),
    ("AK", "Alaska"),
    ("AS", "American Samoa"),
    ("AZ", "Arizona"),
    ("AR", "Arkansas"),
    ("AA", "Armed Forces - Americas"),
    ("AE", "Armed Forces - Europe"),
    ("AP", "Armed Forces - Pacific"),
    ("CA", "California"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DE", "Delaware"),
    ("DC", "District of Columbia"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("GU", "Guam"),
    ("HI", "Hawaii"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("IA", "Iowa"),
    ("KS", "Kansas"),
    ("KY", "Kentucky"),
    ("LA", "Louisiana"),
    ("ME", "Maine"),
    ("MH", "Marshall Islands"),
    ("MD", "Maryland"),
    ("MA", "Massachusetts"),
    ("MI", "Michigan"),
    ("FM", "Micronesia"),
    ("MN", "Minnesota"),
    ("MS", "Mississippi"),
    ("MO", "Missouri"),
    ("MT", "Montana"),
    ("NE", "Nebraska"),
    ("NV", "Nevada"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NY", "New York"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("MP", "Northern Mariana Islands"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PW", "Palau"),
    ("PA", "Pennsylvania"),
    ("PR", "Puerto Rico"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennesse"),
    ("TX", "Texas"),
    ("UT", "Utah"),
    ("VT", "Vermont"),
    ("VI", "Virgin Islands"),
    ("VA", "Virginia"),
    ("WA", "Washington"),
    ("WV", "West Virginia"),
    ("WI", "Wisconsin"),
    ("WY", "Wyoming"),
]
