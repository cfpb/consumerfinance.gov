from wagtail.core import blocks


class QuizAnswer(blocks.StructBlock):
    """Answer blocks to be applied to each question."""
    answer_choice = blocks.CharBlock(
        help_text="An answer that a quiz participant may choose",
        max_length=500)
    choice_letter = blocks.CharBlock(
        help_text=(
            "An optional character to apply to an answer choice"),
        max_length=20,
        required=False)
    answer_response = blocks.RichTextBlock(
        help_text="Our response explaining whether an answer is right",
        features=[
            'ol', 'ul', 'bold', 'italic',
            'link', 'image', 'document-link',
        ],
        blank=True,
        required=False)

    class Meta:
        template = 'paying-for-college/blocks/quiz-answers.html'


class QuizQuestion(blocks.StructBlock):
    """Question blocks that can be added to a guided quiz."""
    subtitle = blocks.CharBlock(
        max_length=500,
        required=False)
    question = blocks.RichTextBlock(
        features=[
            'ol', 'ul', 'bold', 'italic',
            'link', 'image', 'document-link',
        ],
        blank=True,
        required=False)
    answers = blocks.ListBlock(
        QuizAnswer())


class GuidedQuiz(blocks.StructBlock):
    situation = blocks.RichTextBlock(
        features=[
            'ol', 'ul', 'bold', 'italic', 'link', 'image', 'document-link',
        ],
        blank=True,
        required=False,
    )
    questions = blocks.ListBlock(
        QuizQuestion(),
        template='paying-for-college/blocks/quiz-questions.html')
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
