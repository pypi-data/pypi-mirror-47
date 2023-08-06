Server Connection
=================

This package provides a python wrapper for connecting to a resource server


Sample usage
------------

.. code-block:: python

    from msz_svr_conn import ApiConnection

    conn = ApiConnection(
        'localhost:8000',
        '<your oauth id>',
        '<your oauth secret'>,
        '<your user email>',  # or <your user phone number>
        '<your user password',
        token_url='<url to token resource on auth_server>'
    )

    # call a resource server with base url 'localhost:8000'
    conn.call_stub('/api/resource/')

    # call another resource server using the same credentials
    conn.call('http://domain.com/api/resource/')

    # after the access token expires, refresh the token
    conn.refresh('<url to token resource on auth_server>')
