import sql
import sqlConfig



class Recorder():
    def __init__(self):
        pass

    def gps_db(self):
        return sql.get_all(sqlConfig.DATABASE)
    
