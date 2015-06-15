itunes-iap v2
~~~~~~~~~~~~~

Note for v1 users
-----------------

There was breaking change between v1 and v2 APIs.

- Specify version `0.6.6` for latest v1 API when you don't need new APIs.
- Or use `import itunesiap.legacy as itunesiap` instead of `import itunesiap`. (`from itunesiap import xxx` to `from itunesiap.legacy import xxx`)

Quick example
-------------

Create request to create a request to itunes verify api.

    >>> import itunesiap
    >>> try:
    >>>     response = itunesiap.verify(raw_data)  # base64-encoded data
    >>> except InvalidReceipt as e:
    >>>     print 'invalid receipt'
    >>> print response.last_in_app.product_id  # other values are also available as property!

Practical useful values are: product_id, original_transaction_id, quantity, unique_identifier

Quick example with password (Apple Shared Secret)
-------------

Create request to create a request to itunes verify api.

    >>> import itunesiap
    >>> try:
    >>>     response = itunesiap.verify(raw_data, password)  # base64-encoded data
    >>> except itunesiap.exc.InvalidReceipt as e:
    >>>     print 'invalid receipt'
    >>> in_app = response.last_in_app  # Get the latest receipt returned by Apple
    >>> print in_app.product_id  # other values are also available as property!


Verification policy
-------------------

Set verification mode for production or sandbox api. Review mode also available for appstore review.

    >>> import itunesiap
    >>> response = itunesiap.env.review.verify(raw_data)  # `review` enables both production and sandbox for appstore review. `production`, `sandbox`, `review` or `default` possible.

Or

    >>> import itunesiap
    >>> response = itunesiap.verify(raw_data, use_sandbox=True)  # `use_sandbox` allows sandbox receipt. `use_production` allows production receipt.

Or

    >>> import itunesiap
    >>> request = itunesiap.Request(raw_data)
    >>> with request.options(env=itunesiap.env.sandbox):
    >>>     response = request.verify()

