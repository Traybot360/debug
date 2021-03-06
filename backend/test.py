# Set envvars
TEST_PRIVATE_KEY1="0x8467415bb2ba7c91084d932276214b11a3dd9bdb2930fefa194b666dd8020b99"
TEST_PRIVATE_KEY2="0x1d751ded5a32226054cd2e71261039b65afb9ee1c746d055dd699b1150a5befc"

# Set the address file only for ganache
ADDRESS_FILE="~/.ocean/ocean-contracts/artifacts/address.json"

# Set network URL
OCEAN_NETWORK_URL="http://127.0.0.1:8545"

# Create Ocean instance
from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
config = ExampleConfig.get_config()
ocean = Ocean(config)

# Create Alice's wallet
import os
from ocean_lib.web3_internal.wallet import Wallet
alice_private_key = os.getenv('TEST_PRIVATE_KEY1')
alice_wallet = Wallet(ocean.web3, alice_private_key, config.block_confirmations, config.transaction_timeout)

# Publish an NFT token
data_nft = ocean.create_data_nft('NFTToken1', 'NFT1', alice_wallet)
print(f"Created data NFT. Its address is {data_nft.address}")

# Create datatoken related to the above NFT.

datatoken = data_nft.create_datatoken("Datatoken 1", "DT1", from_wallet=alice_wallet)
print(f"Created datatoken. Its address is {datatoken.address}")

# Publish the datatoken
DATA_datatoken = data_nft.create_datatoken("DATA 1", "D1", from_wallet=alice_wallet)
print(f"DATA_datatoken address = '{DATA_datatoken.address}'")

# Specify metadata and services, using the Branin test dataset
DATA_date_created = "2021-12-28T10:55:11Z"
DATA_metadata = {
    "created": DATA_date_created,
    "updated": DATA_date_created,
    "description": "Branin dataset",
    "name": "Branin dataset",
    "type": "dataset",
    "author": "Trent",
    "license": "CC0: PublicDomain",
}

# ocean.py offers multiple file types, but a simple url file should be enough for this example
from ocean_lib.structures.file_objects import UrlFile
DATA_url_file = UrlFile(
    url="https://raw.githubusercontent.com/oceanprotocol/c2d-examples/main/branin_and_gpr/branin.arff"
)

# Encrypt file(s) using provider
DATA_encrypted_files = ocean.assets.encrypt_files([DATA_url_file])

# Set the compute values for compute service
DATA_compute_values = {
    "allowRawAlgorithm": False,
    "allowNetworkAccess": True,
    "publisherTrustedAlgorithms": [],
    "publisherTrustedAlgorithmPublishers": [],
}

# Create the Service
from ocean_lib.services.service import Service
DATA_compute_service = Service(
    service_id="2",
    service_type="compute",
    service_endpoint=ocean.config.provider_url,
    datatoken=DATA_datatoken.address,
    files=DATA_encrypted_files,
    timeout=3600,
    compute_values=DATA_compute_values,
)

# Publish asset with compute service on-chain.
DATA_asset = ocean.assets.create(
    metadata=DATA_metadata,
    publisher_wallet=alice_wallet,
    encrypted_files=DATA_encrypted_files,
    services=[DATA_compute_service],
    data_nft_address=data_nft.address,
    deployed_datatokens=[DATA_datatoken],
)

