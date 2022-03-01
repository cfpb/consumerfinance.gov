from jobmanager.models import City, Office, Region, State


REGIONS = (
    ("MW", "Midwest region"),
    ("NE", "Northeast region"),
    ("SE", "Southeast region"),
    ("WE", "West region"),
)

STATES = (
    ("AL", "Alabama", "SE"),
    ("AK", "Alaska", "WE"),
    ("AZ", "Arizona", "WE"),
    ("AR", "Arkansas", "SE"),
    ("CA", "California", "WE"),
    ("CO", "Colorado", "WE"),
    ("CT", "Connecticut", "NE"),
    ("DC", "District of Columbia", "SE"),
    ("DE", "Delaware", "NE"),
    ("FL", "Florida", "SE"),
    ("GA", "Georgia", "SE"),
    ("HI", "Hawaii", "WE"),
    ("ID", "Idaho", "WE"),
    ("IL", "Illinois", "MW"),
    ("IN", "Indiana", "MW"),
    ("IA", "Iowa", "MW"),
    ("KS", "Kansas", "WE"),
    ("KY", "Kentucky", "MW"),
    ("LA", "Louisiana", "SE"),
    ("ME", "Maine", "NE"),
    ("MD", "Maryland", "SE"),
    ("MA", "Massachusetts", "NE"),
    ("MI", "Michigan", "MW"),
    ("MN", "Minnesota", "MW"),
    ("MS", "Mississippi", "SE"),
    ("MO", "Missouri", "MW"),
    ("MT", "Montana", "WE"),
    ("NE", "Nebraska", "WE"),
    ("NV", "Nevada", "WE"),
    ("NH", "New Hampshire", "NE"),
    ("NJ", "New Jersey", "NE"),
    ("NM", "New Mexico", "WE"),
    ("NY", "New York", "NE"),
    ("NC", "North Carolina", "SE"),
    ("ND", "North Dakota", "WE"),
    ("OH", "Ohio", "MW"),
    ("OK", "Oklahoma", "SE"),
    ("OR", "Oregon", "WE"),
    ("PA", "Pennsylvania", "NE"),
    ("PR", "Puerto Rico", "NE"),
    ("RI", "Rhode Island", "NE"),
    ("SC", "South Carolina", "SE"),
    ("SD", "South Dakota", "WE"),
    ("TN", "Tennessee", "SE"),
    ("TX", "Texas", "SE"),
    ("UT", "Utah", "WE"),
    ("VT", "Vermont", "NE"),
    ("VA", "Virginia", "SE"),
    ("WA", "Washington", "WE"),
    ("WV", "West Virginia", "SE"),
    ("WI", "Wisconsin", "MW"),
    ("WY", "Wyoming", "WE"),
)

OFFICES = (
    ("HQ", "Washington, DC", "Washington", "DC"),
    ("CH", "Chicago, IL", "Chicago", "IL"),
    ("SF", "San Francisco, CA", "San Francisco", "CA"),
    ("NY", "New York, NY", "New York", "NY"),
)

REGIONAL_CITIES = {
    "MW": [
        ("Chicago", "IL"),
        ("Detroit", "MI"),
        ("Minneapolis", "MN"),
        ("St. Louis", "MO"),
        ("Cincinnati", "OH"),
        ("Cleveland", "OH"),
        ("Columbus", "OH"),
        ("Indianapolis", "IN"),
        ("Milwaukee", "WI"),
    ],
    "NE": [
        ("New York City", "NY"),
        ("Philadelphia", "PA"),
        ("Boston", "MA"),
        ("Pittsburgh", "PA"),
        ("Providence", "RI"),
        ("Hartford", "CT"),
        ("Buffalo", "NY"),
        ("Rochester", "NY"),
        ("Bridgeport", "CT"),
        ("Worcester", "MA"),
    ],
    "SE": [
        ("Houston", "TX"),
        ("San Antonio", "TX"),
        ("Dallas", "TX"),
        ("Jacksonville", "FL"),
        ("Austin", "TX"),
        ("Memphis", "TN"),
        ("Baltimore", "MD"),
        ("Charlotte", "NC"),
        ("Atlanta", "GA"),
        ("Virginia Beach", "VA"),
        ("Raleigh", "NC"),
    ],
    "WE": [
        ("Los Angeles", "CA"),
        ("San Francisco", "CA"),
        ("Phoenix", "AZ"),
        ("San Bernardino", "CA"),
        ("Seattle", "WA"),
        ("San Diego", "CA"),
        ("Denver", "CO"),
        ("Portland", "OR"),
        ("Sacramento", "CA"),
        ("Las Vegas", "NV"),
    ],
}


def create_regions():
    for r in REGIONS:
        region_obj, cr = Region.objects.get_or_create(abbreviation=r[0], name=r[1])
        region_obj.save()


def create_states():
    for s in STATES:
        state_obj, cr = State.objects.get_or_create(
            abbreviation=s[0], name=s[1], region_id=s[2]
        )
        state_obj.save()


def create_offices():
    for office in OFFICES:
        office_obj, cr = Office.objects.get_or_create(abbreviation=office[0])
        office_obj.name = office[1]
        if not office_obj.cities.exists():
            related_city = City(name=office[2], state_id=office[3])
            office_obj.cities.add(related_city)
        office_obj.save()


def create_regional_cities():
    for r in REGIONS:
        region_obj = Region.objects.get(abbreviation=r[0])
        for c in REGIONAL_CITIES[r[0]]:
            try:
                region_obj.cities.get(name=c[0], state_id=c[1])
            except City.DoesNotExist:
                related_city = City(name=c[0], state_id=c[1])
                region_obj.cities.add(related_city)
            region_obj.save()


def run():
    create_regions()
    create_states()
    create_offices()
    create_regional_cities()
