from wagtail.wagtailcore import blocks


class QuizAnswers(blocks.StructBlock):
    answers = blocks.ListBlock(
        blocks.StructBlock([
            ('answer_choice', blocks.CharBlock(
                help_text="An answer that a quiz participant may choose",
                max_length=500)),
            ('choice_letter', blocks.CharBlock(
                help_text=(
                    "An optional character to apply to an answer choice"),
                max_length=20,
                required=False)),
            ('answer_response', blocks.RichTextBlock(
                help_text="Our response explaining whether an answer is right",
                features=[
                    'ol', 'ul', 'bold', 'italic',
                    'link', 'image', 'document-link',
                ],
                blank=True,
                required=False,
            )),
        ]),
        label=' ')

    class Meta:
        template = 'paying-for-college/blocks/quiz-answers.html'


class GuidedQuiz(blocks.StructBlock):
    situation = blocks.RichTextBlock(
        features=[
            'ol', 'ul', 'bold', 'italic', 'link', 'image', 'document-link',
        ],
        blank=True,
        required=False,
    )
    questions = blocks.ListBlock(
        blocks.StructBlock([
            ('subtitle', blocks.CharBlock(
                max_length=500, required=False)),
            ('question', blocks.RichTextBlock(
                features=[
                    'ol', 'ul', 'bold', 'italic',
                    'link', 'image', 'document-link',
                ],
                blank=True,
                required=False,
            )),
            ('answers', QuizAnswers()),
        ]))
    summary = blocks.RichTextBlock(
        features=[
            'ol', 'ul', 'bold', 'italic', 'link', 'image', 'document-link',
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = 'grip'
        template = 'paying-for-college/blocks/quiz.html'
        label = 'Guided Quiz'
