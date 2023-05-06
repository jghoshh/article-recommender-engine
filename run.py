from core.app import create_app
from config import ProdConfig, TestConfig

config = TestConfig()

app = create_app(config)

if __name__ == "__main__":
    app.run()