from sql.database import SessionLocal
import sqlalchemy as sa
import pandas as pd
import csv
import uuid

class FileHandler:
    def __init__(self, db: SessionLocal):
        self.db = db

    def process_file(self, file_location, table_name):
        df = pd.read_csv(file_location)
        table_name = self.resolve_table(table_name)
        ddl = pd.io.sql.get_schema(df, table_name, con=self.db)
        print(ddl)
        self.create_table(ddl)
        self.bulk_insert(table_name=table_name, file_location=file_location)

    def bulk_insert(self, table_name, file_location, batchsize=1000):
        # Also need to pass metadata for the table :(
        insert_table = sa.Table(table_name)
        with open(file_location, 'r') as f:
            reader = csv.DictReader(f)
            batch = []
            count = 0
            for row in reader:
                if count >= batchsize:
                    try:
                        self.db.execute(sa.insert(insert_table), batch)
                        self.db.commit()
                    except Exception as e:
                        self.db.rollback()
                        raise e
                    batch = []
                    count = 0
                    # insert rows
                batch.append(row)
                count += 1

    def resolve_table(self, table_name):
        exists = self.check_table(table_name)
        if exists:
            new_name = table_name + uuid.uuid1()[:20].replace('-', '')
        else:
            new_name = table_name
        return new_name

    def check_table(self, table_name):
        # Also need to pass metadata for the table :(
        t = sa.Table(table_name)
        try:
            self.db.execute(t.create(checkfirst=True))
            exists = False
            self.db.execute(t.drop())
        except:
            exists = True
        return exists


    def create_table(self, ddl):
        success = True
        try:
            self.db.execute(ddl)
            self.db.commit()
        except:
            success = False
            self.db.rollback()
        return success

    def close(self):
        self.db.close()

