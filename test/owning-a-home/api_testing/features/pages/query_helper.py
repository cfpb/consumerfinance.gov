

class QueryHelper(object):
    def __init__(self, logger, base_url, mortgage_url):
        self.logger = logger
        self.base_url = base_url
        self.mortgage_url = mortgage_url

        self.house_price = u''
        self.loan_amount = u''
        self.minfico = u''
        self.maxfico = u''
        self.state = u''
        self.rate_structure = u''
        self.loan_term = u''
        self.loan_type = u''
        self.arm_type = u''

        self.mortgage_house_price = u''
        self.mortgage_loan_amount = u''
        self.mortgage_minfico = u''
        self.mortgage_maxfico = u''
        self.mortgage_rate_structure = u''
        self.mortgage_loan_term = u''
        self.mortgage_loan_type = u''
        self.mortgage_arm_type = u''
        self.va_status = u''
        self.va_first_use = u''

    def build(self):

        if (self.house_price == "missing"):
            query_string = {'loan_amount': self.loan_amount,
                            'minfico': self.minfico,
                            'maxfico': self.maxfico,
                            'state': self.state,
                            'rate_structure': self.rate_structure,
                            'loan_term': self.loan_term,
                            'loan_type': self.loan_type,
                            'arm_type': self.arm_type}

        elif (self.loan_amount == "missing"):
            query_string = {'price': self.house_price,
                            'minfico': self.minfico,
                            'maxfico': self.maxfico,
                            'state': self.state,
                            'rate_structure': self.rate_structure,
                            'loan_term': self.loan_term,
                            'loan_type': self.loan_type,
                            'arm_type': self.arm_type}

        elif (self.minfico == "missing"):
            query_string = {'price': self.house_price,
                            'loan_amount': self.loan_amount,
                            'maxfico': self.maxfico,
                            'state': self.state,
                            'rate_structure': self.rate_structure,
                            'loan_term': self.loan_term,
                            'loan_type': self.loan_type,
                            'arm_type': self.arm_type}

        elif (self.maxfico == "missing"):
            query_string = {'price': self.house_price,
                            'loan_amount': self.loan_amount,
                            'minfico': self.minfico,
                            'state': self.state,
                            'rate_structure': self.rate_structure,
                            'loan_term': self.loan_term,
                            'loan_type': self.loan_type,
                            'arm_type': self.arm_type}

        elif (self.state == "missing"):
            query_string = {'price': self.house_price,
                            'loan_amount': self.loan_amount,
                            'minfico': self.minfico,
                            'maxfico': self.maxfico,
                            'rate_structure': self.rate_structure,
                            'loan_term': self.loan_term,
                            'loan_type': self.loan_type,
                            'arm_type': self.arm_type}

        elif (self.rate_structure == "missing"):
            query_string = {'price': self.house_price,
                            'loan_amount': self.loan_amount,
                            'minfico': self.minfico,
                            'maxfico': self.maxfico,
                            'state': self.state,
                            'loan_term': self.loan_term,
                            'loan_type': self.loan_type,
                            'arm_type': self.arm_type}

        elif (self.loan_term == "missing"):
            query_string = {'price': self.house_price,
                            'loan_amount': self.loan_amount,
                            'minfico': self.minfico,
                            'maxfico': self.maxfico,
                            'state': self.state,
                            'rate_structure': self.rate_structure,
                            'loan_type': self.loan_type,
                            'arm_type': self.arm_type}

        elif (self.loan_type == "missing"):
            query_string = {'price': self.house_price,
                            'loan_amount': self.loan_amount,
                            'minfico': self.minfico,
                            'maxfico': self.maxfico,
                            'state': self.state,
                            'rate_structure': self.rate_structure,
                            'loan_term': self.loan_term,
                            'arm_type': self.arm_type}

        elif (self.arm_type == "missing"):
            query_string = {'price': self.house_price,
                            'loan_amount': self.loan_amount,
                            'minfico': self.minfico,
                            'maxfico': self.maxfico,
                            'state': self.state,
                            'rate_structure': self.rate_structure,
                            'loan_term': self.loan_term,
                            'loan_type': self.loan_type}

        else:
            query_string = {'price': self.house_price,
                            'loan_amount': self.loan_amount,
                            'minfico': self.minfico,
                            'maxfico': self.maxfico,
                            'state': self.state,
                            'rate_structure': self.rate_structure,
                            'loan_term': self.loan_term,
                            'loan_type': self.loan_type,
                            'arm_type': self.arm_type}

        return query_string

    def build_mortgage(self):

        if (self.mortgage_house_price == "missing"):
            query_string = {'loan_amount': self.mortgage_loan_amount,
                            'minfico': self.mortgage_minfico,
                            'maxfico': self.mortgage_maxfico,
                            'rate_structure': self.mortgage_rate_structure,
                            'loan_term': self.mortgage_loan_term,
                            'loan_type': self.mortgage_loan_type,
                            'arm_type': self.mortgage_arm_type,
                            'va_status': self.va_status,
                            'va_first_use': self.va_first_use}

        elif (self.mortgage_loan_amount == "missing"):
            query_string = {'price': self.mortgage_house_price,
                            'minfico': self.mortgage_minfico,
                            'maxfico': self.mortgage_maxfico,
                            'rate_structure': self.mortgage_rate_structure,
                            'loan_term': self.mortgage_loan_term,
                            'loan_type': self.mortgage_loan_type,
                            'arm_type': self.mortgage_arm_type,
                            'va_status': self.va_status,
                            'va_first_use': self.va_first_use}

        elif (self.mortgage_minfico == "missing"):
            query_string = {'price': self.mortgage_house_price,
                            'loan_amount': self.mortgage_loan_amount,
                            'maxfico': self.mortgage_maxfico,
                            'rate_structure': self.mortgage_rate_structure,
                            'loan_term': self.mortgage_loan_term,
                            'loan_type': self.mortgage_loan_type,
                            'arm_type': self.mortgage_arm_type,
                            'va_status': self.va_status,
                            'va_first_use': self.va_first_use}

        elif (self.mortgage_maxfico == "missing"):
            query_string = {'price': self.mortgage_house_price,
                            'loan_amount': self.mortgage_loan_amount,
                            'minfico': self.mortgage_minfico,
                            'rate_structure': self.mortgage_rate_structure,
                            'loan_term': self.mortgage_loan_term,
                            'loan_type': self.mortgage_loan_type,
                            'arm_type': self.mortgage_arm_type,
                            'va_status': self.va_status,
                            'va_first_use': self.va_first_use}

        elif (self.mortgage_rate_structure == "missing"):
            query_string = {'price': self.mortgage_house_price,
                            'loan_amount': self.mortgage_loan_amount,
                            'minfico': self.mortgage_minfico,
                            'maxfico': self.mortgage_maxfico,
                            'loan_term': self.mortgage_loan_term,
                            'loan_type': self.mortgage_loan_type,
                            'arm_type': self.mortgage_arm_type,
                            'va_status': self.va_status,
                            'va_first_use': self.va_first_use}

        elif (self.mortgage_loan_term == "missing"):
            query_string = {'price': self.mortgage_house_price,
                            'loan_amount': self.mortgage_loan_amount,
                            'minfico': self.mortgage_minfico,
                            'maxfico': self.mortgage_maxfico,
                            'rate_structure': self.mortgage_rate_structure,
                            'loan_type': self.mortgage_loan_type,
                            'arm_type': self.mortgage_arm_type,
                            'va_status': self.va_status,
                            'va_first_use': self.va_first_use}

        elif (self.mortgage_loan_type == "missing"):
            query_string = {'price': self.mortgage_house_price,
                            'loan_amount': self.mortgage_loan_amount,
                            'minfico': self.mortgage_minfico,
                            'maxfico': self.mortgage_maxfico,
                            'rate_structure': self.mortgage_rate_structure,
                            'loan_term': self.mortgage_loan_term,
                            'arm_type': self.mortgage_arm_type,
                            'va_status': self.va_status,
                            'va_first_use': self.va_first_use}

        elif (self.mortgage_arm_type == "missing"):
            query_string = {'price': self.mortgage_house_price,
                            'loan_amount': self.mortgage_loan_amount,
                            'minfico': self.mortgage_minfico,
                            'maxfico': self.mortgage_maxfico,
                            'rate_structure': self.mortgage_rate_structure,
                            'loan_term': self.mortgage_loan_term,
                            'loan_type': self.mortgage_loan_type,
                            'va_status': self.va_status,
                            'va_first_use': self.va_first_use}

        elif (self.va_status == "missing"):
            query_string = {'price': self.mortgage_house_price,
                            'loan_amount': self.mortgage_loan_amount,
                            'minfico': self.mortgage_minfico,
                            'maxfico': self.mortgage_maxfico,
                            'rate_structure': self.mortgage_rate_structure,
                            'loan_term': self.mortgage_loan_term,
                            'loan_type': self.mortgage_loan_type,
                            'arm_type': self.mortgage_arm_type,
                            'va_first_use': self.va_first_use}

        elif (self.va_first_use == "missing"):
            query_string = {'price': self.mortgage_house_price,
                            'loan_amount': self.mortgage_loan_amount,
                            'minfico': self.mortgage_minfico,
                            'maxfico': self.mortgage_maxfico,
                            'rate_structure': self.mortgage_rate_structure,
                            'loan_term': self.mortgage_loan_term,
                            'loan_type': self.mortgage_loan_type,
                            'arm_type': self.mortgage_arm_type,
                            'va_status': self.va_status}

        else:
            query_string = {'price': self.mortgage_house_price,
                            'loan_amount': self.mortgage_loan_amount,
                            'minfico': self.mortgage_minfico,
                            'maxfico': self.mortgage_maxfico,
                            'rate_structure': self.mortgage_rate_structure,
                            'loan_term': self.mortgage_loan_term,
                            'loan_type': self.mortgage_loan_type,
                            'arm_type': self.mortgage_arm_type,
                            'va_status': self.va_status,
                            'va_first_use': self.va_first_use}

        return query_string
