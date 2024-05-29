from wagtail import hooks
from wagtail.models import Page

from ask_cfpb.models import Answer, AnswerPage


@hooks.register("after_create_page")
def create_answer_id(request, page):
    """
    Create an incremented Answer ID for a new AnswerPage and attach it.

    Also create a sister-language page to keep languages in sync.
    """

    def create_sister_page(new_page, answer_base):
        sister_map = {
            "es": {
                "language": "en",
                "parent": Page.objects.get(slug="ask-cfpb").specific,
                "title_prefix": "English draft of",
            },
            "en": {
                "language": "es",
                "parent": Page.objects.get(slug="obtener-respuestas").specific,
                "title_prefix": "Spanish draft of",
            },
        }
        sister_values = sister_map[new_page.language]
        sister_page = AnswerPage(
            live=False,
            language=sister_values["language"],
            title="{} {}-{}-{}".format(
                sister_values["title_prefix"],
                new_page.title,
                sister_values["language"],
                answer_base.pk,
            ),
            answer_base=answer_base,
        )
        sister_values["parent"].add_child(instance=sister_page)
        return sister_page

    if isinstance(page, AnswerPage) and page.answer_base is None:
        new_answer_base = Answer(last_user=request.user, question=page.title)
        new_answer_base.save()
        new_id = new_answer_base.pk
        page.answer_base = new_answer_base
        page.language = page.get_parent().language
        sister_page = create_sister_page(page, new_answer_base)
        sister_page.save()
        sister_page.save_revision(user=request.user)
        page.title = f"{page.title}-{page.language}-{new_id}"
        page.slug = f"{page.slug}-{page.language}-{new_id}"
        page.save()
        page.save_revision(user=request.user)
