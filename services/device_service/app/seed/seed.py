from sqlalchemy.engine import Connection
from sqlalchemy import text


class SeedDB:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.seed()


    def seed(self):
        self.connection.execute(
            text(
                "INSERT INTO icons (name, icon) VALUES ('robot', '<FontAwesomeIcon icon='fa-solid fa-robot' />');",
                "INSERT INTO icons (name, icon) VALUES ('faucet', '<FontAwesomeIcon icon='fa-solid fa-faucet' />')",
            )
        )
