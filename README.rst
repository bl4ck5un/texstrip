texstrip
========
.. image:: https://badge.fury.io/py/texstrip.svg
    :alt: pypi
    :target: https://badge.fury.io/py/thumbup
.. image:: https://travis-ci.org/bl4ck5un/texstrip.svg?branch=master
    :alt: travis-ci
    :target: https://travis-ci.org/bl4ck5un/texstrip


``texstrip`` is a small tool that strips (removes) comments from TeX sources. I made this tool to relieve myself from manually removing comments when submitting TeX sources to places like arXiv_.

It removes both inline comments (i.e., things between ``%`` and the next ``\n``) and comment environments (i.e., things within ``\begin{comment}`` and ``\end{comment}``),
copies the supplementary files to a new folder for a clean submission.

LaTeX is a complex beast and this tool, despite its humble goal, might fail on corner cases. I fixed many of them during my own use but YMMV. If you do encounter glitches, please submit a PR and let's make it better together!


Getting texstrip
----------------

You'll need `latexpand`.

``texstrip`` can be installed from ``pip`` by

.. code-block::

  pip install texstrip


Usage
-----

(More text to be added here. For now, refer to the help message.)

.. code-block::

  texstrip --help

- TODO: add an example

.. _arXiv: https://arxiv.org/help/faq/whytex