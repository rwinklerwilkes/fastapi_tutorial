from sql.database import SessionLocal
import pandas as pd

class FileHandler:
    def __init__(self, db: SessionLocal):
        self.db = db

    def process_file(self, file_location, filename):
        df = pd.read_csv(file_location)
        ddl = pd.io.sql.get_schema(df, filename, con=self.db)
        print(ddl)

    def create_table(self, ddl):
        pass

    def close(self):
        self.db.close()

