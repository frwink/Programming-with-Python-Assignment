import csv
import pandas as pd
import sqlalchemy 

class CsvReader:
    """
    Write documentation here
    """
    def read_data(self,filepath):
        counter = 0
        with open(filepath, 'r') as file:
            csvreader = csv.reader(file)
            data=[]
            for row in csvreader:
                if counter>0:
                    for i in range(0, len(row)):
                        row[i] = float(row[i])
                    data.append(row)
                counter=counter+1
            return data



class SqlDumper:

    """
    Abstract class used to write pandas frame to to sql
    """
    def __init__(self, sqlengine):
        self.engine = sqlengine

    def dump(self, table_name, frame):
        frame.to_sql(table_name, con= self.engine, index=True, index_label='id', if_exists='replace')


class CsvToSql(SqlDumper):
    """

    """
    def __init__(self, sqlengine):
        SqlDumper.__init__(self,sqlengine)

    def save_csv_to_sqlite(self,table_name, filepath):
        with open(filepath, 'r') as file:
            data_df = pd.read_csv(file)
            self.dump(table_name,data_df)



class Table3Dumper():
    """
    This class writes table 3 data to the database
    """
    def __init__(self, sqlengine, table_name, diffData, idealFnIdx):
        self.engine = sqlengine
        self.table_name = table_name
        self.diffData = diffData
        self.idlFnIdx = idealFnIdx
    
    def write_table3_to_db(self):
        connection = self.engine.connect()
        metadata = sqlalchemy.MetaData()

        emp = sqlalchemy.Table(self.table_name, metadata,
                    sqlalchemy.Column('X', sqlalchemy.Integer()),
                    sqlalchemy.Column('Y1', sqlalchemy.Float()),
                    sqlalchemy.Column('DeltaY', sqlalchemy.Float()),
                    sqlalchemy.Column(f'Funk{self.idlFnIdx}', sqlalchemy.Float())
                    )
        metadata.create_all(self.engine)
        #Inserting record one by one
        for line in  self.diffData:
            dict = {'X':line[0],'Y1':line[1],'DeltaY':line[2], f'Funk{self.idlFnIdx}': line[3]}
            query = sqlalchemy.insert(emp).values(dict) 
            ResultProxy = connection.execute(query)
        
        results = connection.execute(sqlalchemy.select([emp])).fetchall()
        df = pd.DataFrame(results)
        df.columns = results[0].keys()
        df.head(4)
