# from django.core.paginator import InvalidPage, Paginator

from wagtail.wagtailcore.models import PageManager

from forms import HMDA_STATES, HMDA_YEARS, HmdaFilterableForm

from v1.models import BrowsePage


class HmdaExplorerPage(BrowsePage):
    """
    A model for the new HMDA explorer page that displays links to S3 files
    containing HMDA data.
    """

    objects = PageManager()
    template = 'hmda/hmda-explorer.html'

    @classmethod
    def can_create_at(cls, parent):
        # Only allow one of these pages to exist
        # Newer versions of Wagtail have a `max_count` property for this
        return super(HmdaExplorerPage, cls).can_create_at(parent) \
            and not cls.objects.exists()

    def get_context(self, request, *args, **kwargs):
        context = super(HmdaExplorerPage, self).get_context(
            request, *args, **kwargs)

        form = HmdaFilterableForm(request.GET)

        context.update({
            'form': form,
            'action': request.GET.get('action'),
            'states': get_states(request.GET.getlist('states'), HMDA_STATES),
            'years': get_years(request.GET.getlist('years'), HMDA_YEARS),
        })

        return context


def get_states(selected_states, all_states):
    """
    Given a list of state abbreviations, return the full state names.
    """
    states_dict = dict(all_states)
    states = []
    for state in selected_states:
        try:
            states.append(states_dict[state])
        except KeyError:
            pass
    return states


def get_years(selected_years, all_years):
    """
    Return the user's selected years or all years if they didn't provide any.
    """
    return selected_years or list(map(lambda year: year[0], all_years))
