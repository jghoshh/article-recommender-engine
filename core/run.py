from main import create_app
from config import ProdConfig, TestConfig
import os

config = ProdConfig()

app = create_app(config)

if __name__ == "__main__":
    app.run()