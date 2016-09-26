# Including forms into Wagtail page context

Wagtail provides a FormBuilder module, but it cannot be used with subclasses of Page, like our CFGOVPage. For our purposes there is `AbstractFormBlock`, a subclass of StructBlock that implements methods to process a request. If a developer wishes to add a module that includes a form, they only need to follow a few steps in order to get it handled properly:

1. Create the form.
2. Create handler class that implements a method named `process`.
 a. The process method should take in a boolean parameter named `is_submitted` that flags whether or not that particular module has been the source of the request.
 b. The process method should return a dictionary that will be included in the context of the page and a JSONResponse for ajax requests. If a context is returned, this is where the form would go.
3. Create a subclass of `AbstractFormBlock` with any other blocks that are required.
 a. Add the path to the handler class to the block class' Meta handler attribute.
4. Create a template in which to render the form.

Here's an example of a form's block class:
```python
...

class FormBlock(AbstractFormBlock):
    heading = blocks.CharBlock()

    class Meta:
        handler = 'app_name.handlers.handler_class'
        # defaults
        method = 'POST'
        icon = 'form'
```

And an example of a handler class:
```python
...
class ConferenceRegistrationHandler(Handler):
    def process(self, is_submitted):
        if is_submitted:
            form = Form(self.request.POST)
            if form.is_valid():
                return success
            else:
                return fail

        return {'form': Form()}
```
