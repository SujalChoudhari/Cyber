import os, json
import pymongo, dns

class DataBase():
    DEFAULT_SERVER = {
        "emoji_toggle": True,
        "welcome_toggle": False,
        "welcome_channel": 404,
        "mod_role": None
    }
    def __init__(self):
        self.conn_string = f"mongodb+srv://repl-bot:{os.environ['REPL_CYBER']}@cluster0.5iyylus.mongodb.net/?retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(self.conn_string)
        self.database = self.client['database']
        self.colls = {}

    # Unused Methods
    def coll_loc(self,coll):
        return self.colls[coll]

    def _insert(self,coll,data):
        coll = self.coll_loc(coll)
        x = coll.insert_one(data)
        return x.inserted_id

    def _find(self,coll,fields={}):
        coll = self.coll_loc(coll)
        return coll.find({},fields)

    def _reset(self,coll):
        coll = self.coll_loc(coll)
        x = coll.delete_many({})
        return x.deleted_count

    def _query(self,coll,query={"_id":0}):
        coll = self.coll_loc(coll)
        data = coll.find(query)
        for x in data:
            return x

    def _update(self,coll,id,new):
        coll = self.coll_loc(coll)
        query = {"_id":id}
        new_values = { "$set": new }
        coll.update_one(query, new_values)


    # Used Methods
    def create_colls(self,*args):
        for arg in args:
            self.colls[arg] = self.database[arg]
            

    def savedata(self,type,id,data):
        coll = self.coll_loc(type)
        if coll.count_documents({ '_id': id },limit = 1) != 0:
            # exits
            self._update(type,id,data)
        else: #! exists
            self._insert(type,{"_id":id,**data})
    
    def getdata(self,type,id,default={}):
        res = self._query(type,{"_id":id})
        if res == None:
            self.savedata(type,id,default)
            res = default
        return res

    def reset_coll(self,coll):
        return self._reset(coll)

    def find_data(self,coll,fields):
        return self._find(coll, fields)
        



database = DataBase()
database.create_colls("server","bot","user")

