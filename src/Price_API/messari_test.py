# Import Messari API wrapper
from messari.messari import Messari
import time

# Set up Messari instance
# MESSARI_API_KEY = 'add_your_api_key'
messari = Messari()

# Run a quick demo
# markets_df = messari.get_all_markets()
# markets_df.head()

# Di che informazioni ho bisogno? Del prezzo attuale dell'asset crypto.
start = time.time()
all_asset = messari.get_all_assets(limit = 200)
end = time.time()

print(end - start)