from utils import *
import json

import os













def load_agent_config():
    config_path = os.path.join(workdir_path, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            

            assert "COPILOT_PROVIDER_TYPE" in config and config["COPILOT_PROVIDER_TYPE"], "Missing 'COPILOT_PROVIDER_TYPE' in config.json"
            assert "COPILOT_PROVIDER_BASE_URL" in config and config["COPILOT_PROVIDER_BASE_URL"], "Missing 'COPILOT_PROVIDER_BASE_URL' in config.json"
            assert "COPILOT_PROVIDER_API_KEY" in config and config["COPILOT_PROVIDER_API_KEY"], "Missing 'COPILOT_PROVIDER_API_KEY' in config.json"
            assert "COPILOT_MODEL" in config and config["COPILOT_MODEL"], "Missing 'COPILOT_MODEL' in config.json"
            assert "COPILOT_PROVIDER_MODEL_ID" in config and config["COPILOT_PROVIDER_MODEL_ID"], "Missing 'COPILOT_PROVIDER_MODEL_ID' in config.json"
            assert "COPILOT_OFFLINE" in config and config["COPILOT_OFFLINE"], "Missing 'COPILOT_OFFLINE' in config.json"

    else:

        # Initialize agent state if needed
        with open(config_path, "w") as f:
            json.dump({
                "COPILOT_PROVIDER_TYPE": "",
                "COPILOT_PROVIDER_BASE_URL": "",
                "COPILOT_PROVIDER_API_KEY": "",
                "COPILOT_MODEL": "",
                "COPILOT_PROVIDER_MODEL_ID": "",
                "COPILOT_OFFLINE": ""
            }, f, indent=4)  # Save initial config

        raise  FileNotFoundError(f"Config file not found. A new config.json has been created at {config_path}. Please fill in the required fields.")

    return config








if __name__ == "__main__":
    config = load_agent_config()
    print(config)

    print("Agent created or loaded successfully.")
    











