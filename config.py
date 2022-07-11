
# instance identifier - plant-index-database
# username - admin
# pw - admin123
# port - 3306
# hostname - plant-index-database.cyaimo2g0lsu.us-east-2.rds.amazonaws.com

class Config:
    # connecting to the database located at aws servers
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:" \
                                                    "admin123@plant-index-database.cyaimo2g0lsu." \
                                                    "us-east-2.rds.amazonaws.com:" \
                                                    "3306/plant_database"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # connecting to the database located at aws servers (old version of connection)
    # db = pymysql.connect(host='plant-index-database.cyaimo2g0lsu.us-east-2.rds.amazonaws.com', user='admin',
    # password='admin123')
