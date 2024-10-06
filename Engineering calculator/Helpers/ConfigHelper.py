import configparser

# Initialize the configparser
config = configparser.ConfigParser()


# Function to load the mode from the config file
def load_mode(config_file="calculator_config.ini"):
    config.read(config_file)
    if "Settings" in config and "mode" in config["Settings"]:
        return config["Settings"]["mode"]
    else:
        return None


# Function to update the mode in the config file
def update_mode(new_mode, config_file="calculator_config.ini"):
    config.read(config_file)
    if "Settings" not in config:
        config["Settings"] = {}
    config["Settings"]["mode"] = new_mode
    with open(config_file, "w") as configfile:
        config.write(configfile)
    print(f"Mode updated to {new_mode}")
