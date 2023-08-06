from config import Config

config = Config.load_config()


print(config)


Config.save_config(config)