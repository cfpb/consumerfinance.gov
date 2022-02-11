class RegTable:
    """Assemble table from XML and deliver an HTML table."""

    SHELL = (
        '<div class="{table_class}">\n'
        '<table>\n'
        '{header}'
        '<tbody>\n'
        '{body_rows}\n'
        '</tbody>\n'
        '</table>\n'
        '</div>\n')

    def __init__(self, label):
        self.label = label
        self.header_rows = []
        self.body_rows = []
        self.table_class = 'o-table o-table-wrapper__scrolling'
        self.cell_class = 'o-table_cell__right-align'
        self.cell_class_left = 'o-table_cell__left-align'

    def table(self):
        return self.SHELL.format(
            table_class=self.table_class,
            header=self.assemble_header_rows(),
            body_rows="\n".join(self.body_rows)
        )

    def assemble_header_rows(self):
        if not self.header_rows:
            return ''
        header_shell = (
            '<thead>\n'
            '{h_rows}\n'
            '</thead>\n'
        )
        return header_shell.format(h_rows="\n".join(self.header_rows))

    def parse_xml_table(self, table_soup):
        """Convert xml table soup into html elements and store."""

        def clean_row(body_string):
            return body_string.replace(
                '\n', '').replace(
                '<TD', '<td').replace(
                '/TD>', '/td>').replace(
                '<TH', '<th').replace(
                '/TH>', '/th>').replace(
                '<TR', '<tr').replace(
                '/TR>', '/tr>')

        def test_row(row):
            """Determine whether a row is a header row or a body row."""
            cells = row.findChildren()
            if cells[0].name == 'TH':
                return 'header'
            if cells[0].name == 'TD':
                return 'body'

        for row in table_soup.find_all('TR'):
            row_type = test_row(row)
            if row_type == 'header':
                for i, cell in enumerate(row.find_all('TH')):
                    if cell.attrs.get('colspan') or cell.attrs.get('rowspan'):
                        del cell['class']
                    else:
                        if i == 0:
                            del cell['class']
                        else:
                            cell['class'] = self.cell_class
                self.header_rows.append(clean_row(row.prettify()))
            elif row_type == 'body':
                for i, td in enumerate(row.find_all('TD')):
                    if i == 0:
                        del td['class']
                    else:
                        td['class'] = self.cell_class
                self.body_rows.append(clean_row(row.prettify()))
        return('Table is set for {}!'.format(self.label))
