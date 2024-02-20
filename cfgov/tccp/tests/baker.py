from model_bakery import baker


def yes_no_generator():
    return "no"


baker.generators.add("tccp.fields.YesNoBooleanField", yes_no_generator)
