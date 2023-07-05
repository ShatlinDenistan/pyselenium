from sqlalchemy import create_engine
import pandas as pd


def get_data_for_query(sql, connection_string):
    engine = create_engine(connection_string)
    return pd.read_sql(sql, con=engine)
