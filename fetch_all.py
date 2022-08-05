from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://admin:admin123@plant-index-database.cyaimo2g0lsu.us-east-2.rds.amazonaws.com:3306/plant_database")

result = engine.execute("SELECT * from plant_information WHERE plant_id =7")

for row in result:
    print(row['plant_id'], row['plant_name'], row['variety_names'])

