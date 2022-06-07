from flask import Flask, request

# import ocean.ocean_lib.models.test.c2d_test
import c2d_test

app = Flask(__name__)

config = {
    "PORT": 8080,
    "HOST": "0.0.0.0",
}

@app.route('/publish_nft', methods=["POST"])
def part1():
    input_json = request.json
    print(input_json.get("OCEAN_NETWORK_URL"))
    try:
        TEST_PRIVATE_KEY1 = input_json.get("TEST_PRIVATE_KEY1")
        # TEST_PRIVATE_KEY2 = input_json.get("TEST_PRIVATE_KEY2")
        # ADDRESS_FILE = input_json.get("ADDRESS_FILE")
        OCEAN_NETWORK_URL = input_json.get("OCEAN_NETWORK_URL")
    except:
        print(input_json.getKeys())
        return 'Problem getting required params from body',400
    # c2d_test.test()
    c2d_test.publish_nft(TEST_PRIVATE_KEY1, OCEAN_NETWORK_URL)
    return 'Ocean', 200

@app.route('/publish_dataset', methods=["POST"])
def part2():
    input_json = request.json
    print(input_json.get("OCEAN_NETWORK_URL"))
    try:
        TEST_PRIVATE_KEY1 = input_json.get("TEST_PRIVATE_KEY1")
        # TEST_PRIVATE_KEY2 = input_json.get("TEST_PRIVATE_KEY2")
        # ADDRESS_FILE = input_json.get("ADDRESS_FILE")
        OCEAN_NETWORK_URL = input_json.get("OCEAN_NETWORK_URL")
        data_nft_address = input_json.get("data_nft_address")
    except:
        print(input_json.getKeys())
        return 'Problem getting required params from body',400
    # c2d_test.test()
    c2d_test.publish_dataset(TEST_PRIVATE_KEY1, OCEAN_NETWORK_URL,data_nft_address)
    return 'Ocean', 200

@app.route('/publish_alg', methods=["POST"])
def part3():
    input_json = request.json
    print(input_json.get("OCEAN_NETWORK_URL"))
    try:
        TEST_PRIVATE_KEY1 = input_json.get("TEST_PRIVATE_KEY1")
        OCEAN_NETWORK_URL = input_json.get("OCEAN_NETWORK_URL")
    except:
        print(input_json.getKeys())
        return 'Problem getting required params from body',400
    c2d_test.publish_alg(TEST_PRIVATE_KEY1, OCEAN_NETWORK_URL)
    return 'Ocean', 200

@app.route('/allow_alg', methods=["POST"])
def part4():
    input_json = request.json
    print(input_json.get("OCEAN_NETWORK_URL"))
    try:
        TEST_PRIVATE_KEY1 = input_json.get("TEST_PRIVATE_KEY1")
        OCEAN_NETWORK_URL = input_json.get("OCEAN_NETWORK_URL")
        DATA_did = input_json.get("DATA_did")
        ALGO_did = input_json.get("ALGO_did")
    except:
        print(input_json.getKeys())
        return 'Problem getting required params from body',400
    c2d_test.allow_alg(TEST_PRIVATE_KEY1, OCEAN_NETWORK_URL, DATA_did, ALGO_did)
    return 'Ocean', 200

@app.route('/transfer_tokens', methods=["POST"])
def part5():
    input_json = request.json
    print(input_json.get("OCEAN_NETWORK_URL"))
    try:
        TEST_PRIVATE_KEY1 = input_json.get("TEST_PRIVATE_KEY1")
        TEST_PRIVATE_KEY2 = input_json.get("TEST_PRIVATE_KEY2")
        OCEAN_NETWORK_URL = input_json.get("OCEAN_NETWORK_URL")
        DATA_address = input_json.get("DATA_address")
        ALGO_address = input_json.get("ALGO_address")
    except:
        print(input_json.getKeys())
        return 'Problem getting required params from body',400
    c2d_test.transfer_tokens(TEST_PRIVATE_KEY1, TEST_PRIVATE_KEY2, OCEAN_NETWORK_URL, DATA_address, ALGO_address)
    return 'Ocean', 200

@app.route('/start_compute_job', methods=["POST"])
def part6():
    input_json = request.json
    print(input_json.get("OCEAN_NETWORK_URL"))
    try:
        TEST_PRIVATE_KEY2 = input_json.get("TEST_PRIVATE_KEY2")
        OCEAN_NETWORK_URL = input_json.get("OCEAN_NETWORK_URL")
        DATA_did = input_json.get("DATA_did")
        ALGO_did = input_json.get("ALGO_did")

    except:
        print(input_json.getKeys())
        return 'Problem getting required params from body',400
    c2d_test.start_compute_job(DATA_did, ALGO_did, TEST_PRIVATE_KEY2, OCEAN_NETWORK_URL)
    return 'Ocean', 200


if __name__ == '__main__':
    app.run(host=config.get("HOST"), port=config.get("PORT"), debug=True)

