# Trade Gate
<div align="center">
    
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/RastinS/tradeGate/Run%20Unit%20Tests?label=Unit%20Tests&style=flat-square)
![PyPI](https://img.shields.io/pypi/v/tradegate?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tradeGate?style=flat-square)
![GitHub](https://img.shields.io/github/license/rastins/tradegate?style=flat-square)
    
</div>

An algorithmic trading library to use as a gateway to different exchanges.

## How to install
Use this github repository and running ```python setup.py install```, or using pip:
```bash
pip install TradeGate
```

## How to use
Use with a config file in json format. Your config file should look like this:
```json
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
```
You should read this config file as json and give the desired exchange's informations to the main class initializer. Use ```sandbox``` argument to connect to the testnets of exchanges (if it exsits). This is shown below:
```python
from TradeGate import TradeGate
import json

with open('/Users/rustinsoraki/Documents/Projects/tradeGate/config.json') as f:
    config = json.load(f)
    
gate = TradeGate(config['Binance'], sandbox=True)

print(gate.getSymbolTickerPrice('BTCUSDT'))
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Best way to contribute right now is to implement as many exchanges as possible. Make sure all test cases are passing.

## License
[MIT](https://choosealicense.com/licenses/mit/)
