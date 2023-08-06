# flask-commonmark

Add [CommonMark](https://commonmark.org/) processing [filter](http://jinja.pocoo.org/docs/2.10/templates/#filters) to your `Flask` app.

One may notice a similarity to Dan Colish's `Flask-Markdown`, from which I shamelessly copied a bunch of this. Does not have all the nice provisions for extension baked in, but probably does what you need.

Source code may be found at [Gitlab](https://gitlab.com/doug.shawhan/flask-commonmark).

Docs at [readthedocs](https://flask-commonmark.readthedocs.io).

# Installation

```bash
pip install Flask-Commonmark
```

If `pip` is not available on your system, use:

```bash
easy_install Flask-Commonmark
```

# Usage

## Script
```python
from flask_commonmark import Commonmark
cm = Commonmark(app)

@app.route("/commonmark")
def display_commonmark():
    mycm = u"Hello, *commonmark* block."
    return render_template("commonmark.html", mycm=mycm) 
```

## Template

### Inline-style
```html
<html>
{{mycm|commonmark}}
</html>
```

### Block-style
```html
<html>
{% filter commonmark %}
{{mycm}}
{% endfilter %}
</html>
```

## Autoescape

Jinja2's autoescape works as expected. See [tests](https://gitlab.com/doug.shawhan/flask-commonmark/blob/master/tests/test_commonmark.py) for examples.

