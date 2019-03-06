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

    def get_context(self, request, *args, **kwargs):
        context = super(HmdaExplorerPage, self).get_context(
            request, *args, **kwargs)

        form = HmdaFilterableForm(request.GET)
        states = self.get_states(request.GET.getlist('states'), HMDA_STATES)
        years = self.get_years(request.GET.getlist('years'), HMDA_YEARS)

        context.update({
            'form': form,
            'action': request.GET.get('action'),
            'states': states,
            'years': years,
        })

        return context

    def get_states(self, selected_states, all_states):
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

    def get_years(self, selected_years, all_years):
        """
        Return user's selected years or all years if they didn't provide any.
        """
        return selected_years or list(map(lambda year: year[0], all_years))
