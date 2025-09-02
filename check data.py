import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://starwars_misbah:misbah@localhost:5432/starwars_db")
print(pd.read_sql("SELECT COUNT(*) AS rows FROM people", engine))
print(pd.read_sql("SELECT * FROM people LIMIT 10", engine))