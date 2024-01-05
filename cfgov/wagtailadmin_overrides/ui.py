from wagtail.admin.ui.tables import Column


class BooleanColumn(Column):
    """Represents a True/False/None value as a tick/cross/question icon

    TODO: Remove this once we are on Wagtail 5.1.1:
    https://docs.wagtail.org/en/stable/releases/5.1.1.html
    """

    cell_template_name = "wagtailadmin/tables/boolean_cell.html"
