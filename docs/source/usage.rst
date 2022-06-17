Usage
=====

How to install
------------

Use this Github repository by running ```python setup.py install```, or using pip:
```bash
pip install TradeGate
```

How to use
-----------

Use with a config file in JSON format. Your config file should look like this:

.. code-block:: json
    {
        "Binance":
        {
            "exchangeName": "Binance",
            "credentials":
            {
                "main":
                {
                    "futures":
                    {
                        "key": "API-KEY",
                        "secret": "API-SECRET"
                    },
                    "spot":
                    {
                        "key": "API-KEY",
                        "secret": "API-SECRET"
                    }
                },
                "test":
                {
                    "futures":
                    {
                        "key": "API-KEY",
                        "secret": "API-SECRET"
                    },
                    "spot":
                    {
                        "key": "API-KEY",
                        "secret": "API-SECRET"
                    }
                }
            }
        }
    }

You should read this config file as JSON and give the desired exchange information to the main class initializer. Use sandbox argument to connect to the testnets of exchanges (if it exists). This is shown below:

.. code-block:: python
    from TradeGate import TradeGate
    import json

    with open('/path/to/config/file.json') as f:
        config = json.load(f)

    gate = TradeGate(config['Binance'], sandbox=True)

    print(gate.getSymbolTickerPrice('BTCUSDT'))
