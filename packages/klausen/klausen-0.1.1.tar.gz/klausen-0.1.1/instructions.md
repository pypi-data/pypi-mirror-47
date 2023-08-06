## Documentation

We recommend building documentation using [sphinx](http://www.sphinx-doc.org/en/master/), and hosting documentation on [Github pages](https://pages.github.com/) or [read the docs](https://readthedocs.org/). Github pages is easier to configure, while read the docs will build automatically with each pushed commit.

To start the documentation structure, first install `sphinx` using conda or pip. Then change to the `docs` directory, and run `sphinx-quickstart`. We suggest the following **non-default** configuration values (otherwise the default is fine):

* autodoc: automatically insert docstrings from modules (y/n): `y`
* mathjax: include math, rendered in the browser by MathJax (y/n): `y`
* githubpages: create .nojekyll file to publish the document on GitHub pages (y/n): `y` if using Github pages

Note that the default format for writing code is [RestructuredText](http://docutils.sourceforge.net/rst.html), which is different than markdown (what is used in Github, and this readme). You can use [markdown with sphinx](https://www.sphinx-doc.org/en/master/usage/markdown.html).

There are other options for documenting code; the two most popular being [Asciidoctor](https://asciidoctor.org/) and [MkDocs](https://www.mkdocs.org/).

## Testing

Writing good tests is a learned art. People also have strong opinions on what makes good tests! Read some tutorials, learn about fixtures, try things out. Write unit tests, write integration tests, try TDD or BDD. Some tests are better than no tests, but no tests may be better than bad tests. 100% coverage is a journey, not a destination.

## Code quality checks

We strongly recommend using [pytest](https://docs.pytest.org/en/latest/) for testing. It is installable via conda or pip.

### pylama

[pylama](https://github.com/klen/pylama) is a collection of code quality checks which is easy to use. Just install via conda or pip, and then run `pylama <your_library_name>`. You can also run pylama on your tests with `pytest --pylama`.

* For readthedocs, click on the info button next to the badge in https://readthedocs.org/projects/whatever/, and copy the markdown code
* For travis, click on the badge in https://travis-ci.org/BONSAMURAIS/whatever, and copy the markdown code
* For appveyor, go to the projects settings page, and then click on "badges", and copy the markdown code
