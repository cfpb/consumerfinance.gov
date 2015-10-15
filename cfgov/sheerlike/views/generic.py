from django.views.generic.base import TemplateView
from django.http import Http404
from django.template import TemplateDoesNotExist

from elasticsearch import TransportError

from sheerlike.query import get_document 

class SheerTemplateView(TemplateView):
    doc_type = None
    local_name = 'object'
    default_template = None

    def get_template_names(self,*args, **kwargs):
        if self.template_name:
            return [self.template_name]

        request = self.request
        templates = []

        if request.path.endswith('/'):
             templates.append(request.path[1:]+'index.html')
        else:
             templates.append(request.path[1:])
        if 'doc_id' in self.kwargs and self.default_template:
            templates.append(self.default_template)

        return templates

    def get_context_data(self, **kwargs):
        context = super(SheerTemplateView, self).get_context_data(**self.kwargs)
        if 'doc_id' in kwargs:
            doc_id = kwargs.pop('doc_id')
            self.doc_id = doc_id
            try:
                document = get_document(doctype=self.doc_type,
                                        docid=doc_id)
                context[self.local_name] = document

                return context
            except TransportError:
                pass

        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(SheerTemplateView,self).render_to_response(context, **response_kwargs)
        try:
            template = response.resolve_template(response.template_name)
        
        except TemplateDoesNotExist:
            raise Http404("could not find template in " + str(response.template_name))

        if template.template.name == self.default_template and self.local_name not in context:
            raise Http404('fell back to %s, but %s with id %s not found' %
                    (self.default_template, self.doc_type, self.doc_id))
        return response
