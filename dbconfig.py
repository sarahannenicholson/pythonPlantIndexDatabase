from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# instance identifier - plant-index-database
# username - admin
# pw - admin123
# port - 3306
# hostname - plant-index-database.cyaimo2g0lsu.us-east-2.rds.amazonaws.com
import app


class DBConfig:
    # connecting to the database located at aws servers
    engine = create_engine(
        "mysql+pymysql://admin:admin123@plant-index-database.cyaimo2g0lsu.us-east-2.rds.amazonaws.com:3306/plant_database")

    result = engine.execute("SELECT * from plant_information WHERE plant_id =7")

    # connecting to the database located at aws servers (old version of connection)
    # db = pymysql.connect(host='plant-index-database.cyaimo2g0lsu.us-east-2.rds.amazonaws.com', user='admin',
    # password='admin123')

