from django.db import models
from django.template.defaultfilters import slugify


WORKFLOW_STATE = [
    ("APPROVED", "Approved"),
    ("REVISED", "Revised"),
    ("SUBMITTED", "Submitted"),
]


class Calibration(models.Model):
    """Graph values for SSA test cases"""

    created = models.DateTimeField(auto_now_add=True)
    results_json = models.TextField()

    def __unicode__(self):
        return "calibration {0}".format(self.created)


class Step(models.Model):
    title = models.CharField(max_length=500)
    instructions = models.TextField(blank=True)
    instructions_es = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    def trans_instructions(self, language="en"):
        if language == "es":
            return self.instructions_es
        else:
            return self.instructions

    def translist(self):
        """returns list of fields that should be translated"""
        return ["title", "instructions"]


class AgeChoice(models.Model):
    age = models.IntegerField()
    aside = models.CharField(max_length=500)

    def get_subhed(self):
        return (
            "You've chosen age %s. %s Here are some steps \
                to help you in the next few years."
            % (self.age, self.aside)
        )

    def translist(self):
        """returns list of fields that should be translated"""
        return ["aside"]

    class Meta:
        ordering = ["age"]


class Page(models.Model):
    title = models.CharField(max_length=255)
    h1 = models.CharField(max_length=255, blank=True)
    intro = models.TextField(max_length=255)
    h2 = models.CharField(max_length=255, blank=True)
    h3 = models.CharField(max_length=255, blank=True)
    h4 = models.CharField(max_length=255, blank=True)
    step1 = models.ForeignKey(
        Step,
        related_name="step1",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    step2 = models.ForeignKey(
        Step,
        related_name="step2",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    step3 = models.ForeignKey(
        Step,
        related_name="step3",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    final_steps = models.TextField(blank=True)

    def translist(self):
        """returns list of fields that should be translated"""
        return ["title", "h1", "intro", "h2", "h3", "h4", "final_steps"]

    def __unicode__(self):
        return self.title


class Tooltip(models.Model):
    title = models.CharField(max_length=500)
    text = models.TextField(max_length=255, blank=True)

    def translist(self):
        """returns list of fields that should be translated"""
        return ["text"]

    def __unicode__(self):
        return self.title


POHEADER = [
    'msgid ""\n',
    'msgstr ""\n',
    '"MIME-Version: 1.0\\n"\n',
    '"Content-Type: text/plain; charset=UTF-8\\n"\n',
    '"Content-Transfer-Encoding: 8bit\\n"\n',
    '"Project-Id-Version: retirement\\n"\n',
    '"Language: es\\n"\n\n',
]


class Question(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(blank=True)
    question = models.TextField(blank=True)
    answer_yes_a_subhed = models.CharField(
        max_length=255, blank=True, help_text="Under 50"
    )
    answer_yes_a = models.TextField(blank=True, help_text="Under 50")
    answer_yes_b_subhed = models.CharField(
        max_length=255, blank=True, help_text="50 and older"
    )
    answer_yes_b = models.TextField(blank=True, help_text="50 and older")
    answer_no_a_subhed = models.CharField(
        max_length=255, blank=True, help_text="Under 50"
    )
    answer_no_a = models.TextField(blank=True, help_text="Under 50")
    answer_no_b_subhed = models.CharField(
        max_length=255, blank=True, help_text="50 and older"
    )
    answer_no_b = models.TextField(blank=True, help_text="50 and older")
    answer_unsure_a_subhed = models.CharField(
        max_length=255, blank=True, help_text="Under 50"
    )
    answer_unsure_a = models.TextField(blank=True, help_text="Under 50")
    answer_unsure_b_subhed = models.CharField(
        max_length=255, blank=True, help_text="50 and older"
    )
    answer_unsure_b = models.TextField(blank=True, help_text="50 and older")
    workflow_state = models.CharField(
        max_length=255, choices=WORKFLOW_STATE, default="SUBMITTED"
    )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title).replace("-", "_")
        super(Question, self).save(*args, **kwargs)

    def translist(self):
        """returns list of fields that should be translated"""
        fieldlist = [
            "question",
            "answer_yes_a_subhed",
            "answer_yes_a",
            "answer_yes_b_subhed",
            "answer_yes_b",
            "answer_no_a_subhed",
            "answer_no_a",
            "answer_no_b_subhed",
            "answer_no_b",
            "answer_unsure_a_subhed",
            "answer_unsure_a",
            "answer_unsure_b_subhed",
            "answer_unsure_b",
        ]
        return fieldlist

    def dump_translation_text(self, output=False, outfile=None):
        """
        translation utility

        returns a list of phrases to be translated,
        or outputs a utf-8 .po file to /tmp/
        """
        fieldlist = self.translist()
        phrases = [
            self.__getattribute__(attr)
            for attr in fieldlist
            if self.__getattribute__(attr)
        ]

        if output is True:
            outfile = outfile or "/tmp/%s.po" % self.slug
            with open(outfile, "wb") as f:
                for line in POHEADER:
                    f.write(line.encode("utf-8"))
                for phrase in phrases:
                    f.write("#: templates/claiming.html\n".encode("utf-8"))
                    f.write(str('msgid "%s"\n' % phrase).encode("utf-8"))
                    f.write('msgstr ""\n\n'.encode("utf-8"))
        else:
            return phrases
