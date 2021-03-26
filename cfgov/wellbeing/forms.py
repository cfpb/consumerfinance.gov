from django import forms


class FWBScore(object):
    HIGH = 95
    LOW = 14
    AVG = 54

    def __init__(self, score):
        self.score = score

    def __str__(self):
        return str(self.score)

    @classmethod
    def avg(cls):
        return cls(cls.AVG)

    @property
    def pct(self):
        return ((self.score - self.LOW) / (self.HIGH - self.LOW)) * 100

    @property
    def color(self):
        if self.score < 40:
            return '#e05f21'
        elif self.score < 50:
            return '#f9921c'
        elif self.score < 60:
            return '#a6a329'
        elif self.score < 70:
            return '#44a839'
        else:  # score >= 70
            return '#398c7a'


class ResultsForm(forms.Form):
    question_1 = forms.IntegerField()  # update field names in markup to use _
    question_2 = forms.IntegerField()
    question_3 = forms.IntegerField()
    question_4 = forms.IntegerField()
    question_5 = forms.IntegerField()
    question_6 = forms.IntegerField()
    question_7 = forms.IntegerField()
    question_8 = forms.IntegerField()
    question_9 = forms.IntegerField()
    question_10 = forms.IntegerField()
    age = forms.ChoiceField(
        choices=(
            ('18-61', '18-61'),
            ('62-plus', '62+')
        )
    )
    method = forms.ChoiceField(
        choices=(
            ('read-self', 'I read and answered the questions myself'),
            ('read-to-me', 'I read the questions to someone else and recorded '
                           'their answers')
        )
    )

    def clean(self):
        cleaned_data = super(ResultsForm, self).clean()

        if self._errors:
            return

        SCORING = {
            'read-self': {
                '18-61': [
                    14, 19, 22, 25, 27, 29, 31, 32, 34, 35, 37, 38, 40, 41, 42,
                    44, 45, 46, 47, 49, 50, 51, 52, 54, 55, 56, 58, 59, 60, 62,
                    63, 65, 66, 68, 69, 71, 73, 75, 78, 81, 86
                ],
                '62-plus': [
                    14, 20, 24, 26, 29, 31, 33, 35, 36, 38, 39, 41, 42, 44, 45,
                    46, 48, 49, 50, 52, 53, 54, 56, 57, 58, 60, 61, 63, 64, 66,
                    67, 69, 71, 73, 75, 77, 79, 82, 84, 88, 95
                ]
            },
            'read-to-me': {
                '18-61': [
                    16, 21, 24, 27, 29, 31, 33, 34, 36, 38, 39, 40, 42, 43, 44,
                    45, 47, 48, 49, 50, 52, 53, 54, 55, 57, 58, 59, 60, 62, 63,
                    65, 66, 68, 70, 71, 73, 76, 78, 81, 85, 91
                ],
                '62-plus': [
                    18, 23, 26, 28, 30, 32, 33, 35, 36, 38, 39, 40, 41, 43, 44,
                    45, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 60, 61,
                    62, 64, 65, 67, 68, 70, 72, 75, 77, 81, 87
                ]
            }
        }

        answers = []
        answer_values = 0

        for i in range(1, 11):
            q = "question_%s" % i
            answers.append(int(cleaned_data.get(q)))
            answer_values += int(cleaned_data.get(q))

        method = cleaned_data.get('method')
        age = cleaned_data.get('age')
        user_score = FWBScore(SCORING[method][age][answer_values])

        cleaned_data['answers'] = answers
        cleaned_data['user_score'] = user_score
