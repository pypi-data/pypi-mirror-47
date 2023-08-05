Pastoke
===========
Script for log, clear or replace clipboard with using 'pyperclip'

Install
===========

.. code-block:: python

    pip install pastoke

Usage
===========

.. code-block:: python

    from pastoke import log_changes, clear_clipboard, replace_clipboard

    # log clipboard to log.txt file. Default path is python exe dir
    log_changes()
    
    # clear clipboard
    clear_clipboard()
    
    # replace clipboard with specified phrase
    replace_clipboard(search='test', thing='trick')
    