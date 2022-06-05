#
# Copyright 2022 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#
import os
import time
import pytest
from decimal import Decimal

from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.structures.file_objects import UrlFile
from ocean_lib.services.service import Service

@pytest.mark.unit
def test_main():
    """Tests the events' properties."""
    print ("Starting tests")
    print("testing...")
    # Set envvars
    TEST_PRIVATE_KEY1="0x8467415bb2ba7c91084d932276214b11a3dd9bdb2930fefa194b666dd8020b99"
    TEST_PRIVATE_KEY2="0x1d751ded5a32226054cd2e71261039b65afb9ee1c746d055dd699b1150a5befc"

    # Set the address file only for ganache
    ADDRESS_FILE="~/.ocean/ocean-contracts/artifacts/address.json"

    # Set network URL
    OCEAN_NETWORK_URL="http://127.0.0.1:8545"
    
    config = ExampleConfig.get_config()
    ocean = Ocean(config)
    alice_private_key = os.getenv('TEST_PRIVATE_KEY1')
    alice_wallet = Wallet(ocean.web3, alice_private_key, config.block_confirmations, config.transaction_timeout)
    data_nft = ocean.create_data_nft('NFTToken1', 'NFT1', alice_wallet)
    print(f"Created data NFT. Its address is {data_nft.address}")

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

    print(f"DATA_asset did = '{DATA_asset.did}'")

    # Publish the algorithm NFT token
    ALGO_nft_token = ocean.create_data_nft("NFTToken1", "NFT1", alice_wallet)
    print(f"ALGO_nft_token address = '{ALGO_nft_token.address}'")

    # Publish the datatoken
    ALGO_datatoken = ALGO_nft_token.create_datatoken("ALGO 1", "A1", from_wallet=alice_wallet)
    print(f"ALGO_datatoken address = '{ALGO_datatoken.address}'")

    # Specify metadata and services, using the Branin test dataset
    ALGO_date_created = "2021-12-28T10:55:11Z"

    ALGO_metadata = {
        "created": ALGO_date_created,
        "updated": ALGO_date_created,
        "description": "gpr",
        "name": "gpr",
        "type": "algorithm",
        "author": "Trent",
        "license": "CC0: PublicDomain",
        "algorithm": {
            "language": "python",
            "format": "docker-image",
            "version": "0.1",
            "container": {
                "entrypoint": "python $ALGO",
                "image": "oceanprotocol/algo_dockers",
                "tag": "python-branin",
                "checksum": "44e10daa6637893f4276bb8d7301eb35306ece50f61ca34dcab550",
            },
        }
    }
    ALGO_url_file = UrlFile(
        url="https://raw.githubusercontent.com/oceanprotocol/c2d-examples/main/branin_and_gpr/gpr.py"
    )

    # Encrypt file(s) using provider
    ALGO_encrypted_files = ocean.assets.encrypt_files([ALGO_url_file])

    # Publish asset with compute service on-chain.
    # The download (access service) is automatically created, but you can explore other options as well
    ALGO_asset = ocean.assets.create(
        metadata=ALGO_metadata,
        publisher_wallet=alice_wallet,
        encrypted_files=ALGO_encrypted_files,
        data_nft_address=ALGO_nft_token.address,
        deployed_datatokens=[ALGO_datatoken],
    )

    print(f"ALGO_asset did = '{ALGO_asset.did}'")

    compute_service = DATA_asset.services[0]
    compute_service.add_publisher_trusted_algorithm(ALGO_asset)
    DATA_asset = ocean.assets.update(DATA_asset, alice_wallet)

    bob_wallet = Wallet(
    ocean.web3,
    os.getenv("TEST_PRIVATE_KEY2"),
    config.block_confirmations,
    config.transaction_timeout,
    )
    print(f"bob_wallet.address = '{bob_wallet.address}'")

    # Alice mints DATA datatokens and ALGO datatokens to Bob.
    # Alternatively, Bob might have bought these in a market.
    DATA_datatoken.mint(bob_wallet.address, ocean.to_wei(5), alice_wallet)
    ALGO_datatoken.mint(bob_wallet.address, ocean.to_wei(5), alice_wallet)

    # Convenience variables
    DATA_did = DATA_asset.did
    ALGO_did = ALGO_asset.did

    # Operate on updated and indexed assets
    DATA_asset = ocean.assets.resolve(DATA_did)
    ALGO_asset = ocean.assets.resolve(ALGO_did)

    compute_service = DATA_asset.services[0]
    algo_service = ALGO_asset.services[0]
    environments = ocean.compute.get_c2d_environments(compute_service.service_endpoint)

    from datetime import datetime, timedelta
    from ocean_lib.models.compute_input import ComputeInput

    DATA_compute_input = ComputeInput(DATA_asset, compute_service)
    ALGO_compute_input = ComputeInput(ALGO_asset, algo_service)

    # Pay for dataset and algo for 1 day
    datasets, algorithm = ocean.assets.pay_for_compute_service(
        datasets=[DATA_compute_input],
        algorithm_data=ALGO_compute_input,
        consume_market_order_fee_address=bob_wallet.address,
        wallet=bob_wallet,
        compute_environment=environments[0]["id"],
        valid_until=int((datetime.utcnow() + timedelta(days=1)).timestamp()),
        consumer_address=environments[0]["consumerAddress"],
    )
    assert datasets, "pay for dataset unsuccessful"
    assert algorithm, "pay for algorithm unsuccessful"

    # Start compute job
    job_id = ocean.compute.start(
        consumer_wallet=bob_wallet,
        dataset=datasets[0],
        compute_environment=environments[0]["id"],
        algorithm=algorithm,
    )
    print(f"Started compute job with id: {job_id}")

    # Wait until job is done
    succeeded = False
    for _ in range(0, 200):
        status = ocean.compute.status(DATA_asset, compute_service, job_id, bob_wallet)
        if status.get("dateFinished") and Decimal(status["dateFinished"]) > 0:
            succeeded = True
            break
        time.sleep(5)

test_main()