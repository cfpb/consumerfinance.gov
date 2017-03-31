from knowledgebase.models import Question

# A starter list of ask IDs redirecting from [0] to [1]
# requested in Jira issue PLATFORM-18
FROM_TO = [
    (311, 5),
    (1267, 5),
    (1281, 5),
    (1261, 313),
    (317, 315),
    (310, 309),
    (1259, 309),
    (1115, 1813),
    (1375, 31),
    (1353, 1341),
    (1375, 1341),
    (1255, 1253),
    (16, 1253),
    (17, 1253),
    (1303, 314),
    (1451, 1343),
    (1453, 1343),
    (1455, 1343),
    (1069, 1017),
]


def assemble_legacy_redirects():
    """Add from-to Ask IDs from legacy redirects"""
    global FROM_TO
    for line in LEGACY_REDIRECTS:
        fields = line.split(' ')
        ask_id = int(fields[2].split('/')[2])
        redirect_id = int(fields[3].split('/')[2])
        FROM_TO.append((ask_id, redirect_id))

# we don't need this Spanish URL pattern, but keeping it for now
# ask_id = line.split(' ')[2].split('/')[5]


def get_question(ask_id):
    try:
        q = Question.objects.get(id=ask_id)
    except Question.DoesNotExist:
        return False
    else:
        return q


def get_ask_info(ask_id):
    missing_id = None
    ask_info = {'english_answer': '', 'spanish_answer': ''}
    q = get_question(ask_id)
    if not q:
        missing_id = ask_id
        print("Failed to find a question for ID {}".format(ask_id))
    else:
        if q.get_english_answer():
            ask_info['english_answer'] = q.get_english_answer().answer
        if q.get_spanish_answer():
            ask_info['spanish_answer'] = q.get_spanish_answer().answer
    return ask_info, missing_id


def assemble_answer_info():
    missing_ids = []
    answer_info = {}
    for pair in FROM_TO:
        ask_id = pair[0]
        redirect_id = pair[1]
        answer_info[ask_id], missing = get_ask_info(ask_id)
        if missing:
            missing_ids.append(missing)
        answer_info[ask_id]['redirect_id'] = redirect_id
    return (answer_info, missing_ids)

LEGACY_REDIRECTS = [
    "Redirect permanent /askcfpb/125 /askcfpb/127",
    "Redirect permanent /askcfpb/126 /askcfpb/127",
    "Redirect permanent /askcfpb/150 /askcfpb/144",
    "Redirect permanent /askcfpb/145 /askcfpb/144",
    "Redirect permanent /askcfpb/171 /askcfpb/144",
    "Redirect permanent /askcfpb/169 /askcfpb/148",
    "Redirect permanent /askcfpb/149 /askcfpb/143",
    "Redirect permanent /askcfpb/151 /askcfpb/1965",
    "Redirect permanent /askcfpb/138 /askcfpb/153",
    "Redirect permanent /askcfpb/139 /askcfpb/1845",
    "Redirect permanent /askcfpb/194 /askcfpb/172",
    "Redirect permanent /askcfpb/156 /askcfpb/155",
    "Redirect permanent /askcfpb/191 /askcfpb/184",
    "Redirect permanent /askcfpb/142 /askcfpb/141",
    "Redirect permanent /askcfpb/173 /askcfpb/1991",
    "Redirect permanent /askcfpb/174 /askcfpb/1983",
    "Redirect permanent /askcfpb/165 /askcfpb/1965",
    "Redirect permanent /askcfpb/729 /askcfpb/825",
    "Redirect permanent /askcfpb/741 /askcfpb/759",
    "Redirect permanent /askcfpb/793 /askcfpb/751",
    "Redirect permanent /askcfpb/829 /askcfpb/743",
    "Redirect permanent /askcfpb/879 /askcfpb/831",
    "Redirect permanent /askcfpb/885 /askcfpb/759",
    "Redirect permanent /askcfpb/1173 /askcfpb/1171",
    "Redirect permanent /askcfpb/1175 /askcfpb/1171",
    "Redirect permanent /askcfpb/735 /askcfpb/2047",
    "Redirect permanent /askcfpb/737 /askcfpb/2047",
    "Redirect permanent /askcfpb/775 /askcfpb/2047",
    "Redirect permanent /askcfpb/847 /askcfpb/815",
    "Redirect permanent /askcfpb/859 /askcfpb/865",
    "Redirect permanent /askcfpb/863 /askcfpb/857",
    "Redirect permanent /askcfpb/867 /askcfpb/865",
    "Redirect permanent /askcfpb/869 /askcfpb/865",
    "Redirect permanent /askcfpb/1177 /askcfpb/1171",
    "Redirect permanent /askcfpb/1183 /askcfpb/1171",
    "Redirect permanent /askcfpb/1189 /askcfpb/1191",
    "Redirect permanent /askcfpb/1193 /askcfpb/1191",
    "Redirect permanent /askcfpb/1197 /askcfpb/1195",
    "Redirect permanent /askcfpb/1199 /askcfpb/1191",
    "Redirect permanent /askcfpb/1203 /askcfpb/1191",
    "Redirect permanent /askcfpb/875 /askcfpb/873",
    "Redirect permanent /askcfpb/387 /askcfpb/381",
    "Redirect permanent /askcfpb/389 /askcfpb/381",
    "Redirect permanent /askcfpb/391 /askcfpb/381",
    "Redirect permanent /askcfpb/397 /askcfpb/381",
    "Redirect permanent /askcfpb/399 /askcfpb/381",
    "Redirect permanent /askcfpb/431 /askcfpb/381",
    "Redirect permanent /askcfpb/435 /askcfpb/433",
    "Redirect permanent /askcfpb/467 /askcfpb/427",
    "Redirect permanent /askcfpb/469 /askcfpb/2053",
    "Redirect permanent /askcfpb/477 /askcfpb/2053",
    "Redirect permanent /askcfpb/481 /askcfpb/479",
    "Redirect permanent /askcfpb/483 /askcfpb/2053",
    "Redirect permanent /askcfpb/485 /askcfpb/2053",
    "Redirect permanent /askcfpb/487 /askcfpb/2053",
    "Redirect permanent /askcfpb/489 /askcfpb/2053",
    "Redirect permanent /askcfpb/491 /askcfpb/2053",
    "Redirect permanent /askcfpb/493 /askcfpb/2053",
    "Redirect permanent /askcfpb/495 /askcfpb/2053",
    "Redirect permanent /askcfpb/497 /askcfpb/2053",
    "Redirect permanent /askcfpb/499 /askcfpb/2053",
    "Redirect permanent /askcfpb/535 /askcfpb/381"
]


def run():
    assemble_legacy_redirects()
    (answer_info, missing_ids) = assemble_answer_info()
    return (answer_info, missing_ids)

missing = [
    397,
    399,
    431,
    735,
    737,
    741,
    775,
    793,
    829,
    847,
    859,
    863,
    867,
    869,
    875,
    879,
    885,
    1173,
    1175,
    1177,
    1183,
    1189,
    1193,
    1197,
    1199,
    1203
]
