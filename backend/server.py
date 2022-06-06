from flask import Flask, request

# import ocean.ocean_lib.models.test.c2d_test
import c2d_test

app = Flask(__name__)

config = {
    "PORT": 8080,
    "HOST": "0.0.0.0",
}

@app.route('/publish_nft', methods=["POST"])
def index():
    input_json = request.json
    print(input_json.get("OCEAN_NETWORK_URL"))

    # # Set envvars
    TEST_PRIVATE_KEY1="0x8467415bb2ba7c91084d932276214b11a3dd9bdb2930fefa194b666dd8020b99"
    TEST_PRIVATE_KEY2="0x1d751ded5a32226054cd2e71261039b65afb9ee1c746d055dd699b1150a5befc"

    # Set the address file only for ganache
    # ADDRESS_FILE="~/.ocean/ocean-contracts/artifacts/address.json"

    # Set network URL
    OCEAN_NETWORK_URL="http://127.0.0.1:8545"
    try:
        TEST_PRIVATE_KEY1 = input_json.get("TEST_PRIVATE_KEY1")
        TEST_PRIVATE_KEY2 = input_json.get("TEST_PRIVATE_KEY2")
        ADDRESS_FILE = input_json.get("ADDRESS_FILE")
        OCEAN_NETWORK_URL = input_json.get("OCEAN_NETWORK_URL")
    except:
        print(input_json.getKeys())
        return 'Problem getting required params from body',400
    # c2d_test.test()
    c2d_test.test_main(TEST_PRIVATE_KEY1, TEST_PRIVATE_KEY2, ADDRESS_FILE, OCEAN_NETWORK_URL)
    return 'Ocean', 200

if __name__ == '__main__':
    app.run(host=config.get("HOST"), port=config.get("PORT"), debug=True)
