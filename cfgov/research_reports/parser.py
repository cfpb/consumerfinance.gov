import subprocess

def get_pandoc_output(report_file_location):
    pandoc_command = ["pandoc", "-f", "docx", "-t", "html", report_file_location]
    result = subprocess.run(pandoc_command, stdout=subprocess.PIPE, universal_newlines=True)
    return result.stdout

def save_page(page):
    revision = page.save_revision()
    page.save()

def parse_document(page, report_file):
    local_file_path = report_file.file.path
    report_html = get_pandoc_output(local_file_path)
    page.main_content = report_html
    save_page(page)
