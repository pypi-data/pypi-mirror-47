VHDL Style Guide (VSG)
======================

Overview
--------

VSG was created after participating in a code review.
A real issue in the code was masked by a coding style issue.
A finding was created for the style issue, while the real issue was missed.
When the code was re-reviewed, the real issue was discovered.

Depending on your process, style issues can take a lot of time to resolve.

#. Create finding/ticket/issue
#. Disposition finding/ticket/issue
#. Fix
#. Verify fix

Spending less time on style issues leaves more time to analyze the substance of the code.
This ultimately reduces the amount of time performing code reviews.
It also allows reviewers to focus on the substance of the code.
This will result in a higher quality code base.

Key Benefits
------------

* Define VHDL coding standards
* Makes coding standards visible to everyone
* Improve code reviews
* Quickly bring code up to current standards

VSG allows the style of the code to be defined and enforced over part or the entire code base.
Configurations allow for multiple coding standards.

Key Features
------------

* Command line tool

  * integrate into continuous integration flow

* Reports and fixes issues found

  * whitespace

    * horizontal
    * vertical

  * upper and lower case
  * keyword alignments
  * etc...

* Fully configurable rules via JSON or YAML configuration file

  * Disable rules
  * Alter behavior of existing rules
  * Change phase of execution

* Localize rule sets

  * Create your own rules using python
  * Use existing rules as a template
  * Fully integrates into base rule set

Installation
------------

You can get the latest released version of VSG via **pip**.

.. code-block:: bash

    pip install vsg

The latest development version can be cloned...

.. code-block:: bash

    git clone https://github.com/jeremiah-c-leary/vhdl-style-guide.git

...and then installed locally...

.. code-block:: bash

    python setup.py install

