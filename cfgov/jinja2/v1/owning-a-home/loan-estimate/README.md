# Form Explainer

Form Explainer is a Jinja macro that you can use with Sheer.

## Setting up a new Form Explainer

### Step 1: Building the overlay shapes and starting some content in Illustrator

Start by creating a separate Illustrator file for each form page.
In each file create your ractangular overlays.
Name each rectangle by editing its layer name.
The naming convetion is: `[category]_[id]`,
where `[category]` is one of the following: "checklist", "alerts", "definitions",
and `[id]` is a semi-unique name.
It only needs to be semi-unique because when rendered in the HTML,
the page number and the category will get prefixed to the `[id]` that you choose.
Here are some examples of valid names:

```
checklist_estimate
checklist_loan-estimate
alerts_estimate
alerts_loan-estimate
definitions_estimate
definitions_loan-estimate
```

Save the files as SVG's,
but leave out the image of the form,
all we need are the overlays.

Convert the SVG's into Form Explainer-compliant JSON files.
"Form Explainer-compliant JSON" simply means that it has all of the properties
that Form Explainer requires.
We will use the data structure of these JSON files to store the overlay
dimensions and coordinates as well as the rest of the content needed to run a
Form Explainer.
A tool for converting from SVG to a Form Explainer-compliant JSON file
can be found at <https://github.com/himedlooff/form-explainer-svg-parser>.

Note that the JSON file is an intermediary step.
It won't get used directly and the rest of the content will be added in a later step.

### Step 2: Creating the end-HTML file

Create new Jinja HTML files for each page in the form.
These will be the end-files used by Sheer.
The files should have this intitial structure:

```jinja
{% set data = {

"img": "path-to-an-image-of-a-form-page.extension",
"terms":
[]

} %}
```

### Step 3: Moving the JSON into the HTML file and filling in the rest of the content

Replace the `terms` array from **Step 2** with the JSON array created in **Step 1**.
You should end up with something like this:

```jinja
{% set data = {

"img": "path-to-an-image-of-a-form-page.extension",
"terms":
[
    {
        "term": "",
        "definition": "",
        "id": "testing",
        "category": "checklist",
        "left": "44.68%",
        "top": "11.95%",
        "width": "19.86%",
        "height": "4.50%"
    },
    {
        "term": "",
        "definition": "",
        "id": "testing",
        "category": "checklist",
        "left": "69.93%",
        "top": "10.20%",
        "width": "24.11%",
        "height": "10.31%"
    }
]

} %}
```

You can now start filling in the rest of the content.
The `term` property is what you will see on the right side of the form.
The `definition` property is what you will see in the right side of the form when
expanding a `term`.
`definition`'s can be empty.
If they are empty, then `term` will not have the o-expandable functionality.

### Step 4: Bringing it all together

Make an HTML file for your form and import the Form Explainer macros.

```jinja
{% import "form-explainer.html" as form_explainer %}
```

Then import each HTML file you created in steps 1-3.

```jinja
{% from "loan-estimate-1.html" import data as page_1 %}
{% from "loan-estimate-2.html" import data as page_2 %}
{% from "loan-estimate-3.html" import data as page_3 %}
```

Finally, render the Form Explainer by calling its `render` function
and passing it an array of your form pages.

```jinja
{{ form_explainer.render([ page_1, page_2, page_3 ]) }}
```
