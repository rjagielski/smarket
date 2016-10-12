from smarket.client import SMarketClient


client = SMarketClient()

try:
    while True:
        client.run_cli()
except KeyboardInterrupt:
    pass
