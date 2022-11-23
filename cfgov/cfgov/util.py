def admin_emails(delimited_list):
    emails = []

    if delimited_list:
        for email in delimited_list.split(";"):
            name_email = email.split("@")
            emails.append((name_email[0], email))

    return emails
