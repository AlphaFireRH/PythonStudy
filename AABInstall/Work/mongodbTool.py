#!use/bin/env python3
# -*- coding utf-8 -*-


from pymongo import MongoClient

settings = {
    "ip": '192.168.1.210',
    # 'www.alphaFire.win',  # ip
    "port": 32768,  # 端口
    "db_name": "test",  # 默认数据库名字
    "collection_name": "test_col"  # 默认集合名字
}


class MyMongoDB(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], settings["port"])
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.my_col = self.db[settings["collection_name"]]

    # 获取连接
    def GetClient(self):
        return self.conn

    # 获取库
    def GetDB(self):
        return self.db

    # 设置取库
    def SetDB(self, db):
        self.db = db

    # 获取库
    def GetDBWithName(self, dbName):
        db = self.conn[dbName]
        return db

    # 数据库是否存在
    def DBIsExists(self, dbName):
        dblist = self.conn.list_database_names()
        if dbName in dblist:
            return True
        return False

    # 获取集合
    def GetCollection(self):
        return self.my_col

    # 设置集合
    def SetCollection(self, col):
        self.my_col = col

    # 获取集合
    def GetCollectionWithName(self, collectionName):
        collection = self.db[collectionName]
        return collection

    # 获取集合
    def GetCollectionWithDatabaseAndName(self, db, collectionName):
        collection = db[collectionName]
        return collection

    # 集合是否存在
    def CollectionIsExists(self, db, collectionName):
        collectionlist = self.conn.list_collection_names()
        if collectionName in collectionlist:
            return True
        return False

    # 插入字典
    def InsertDict(self, dict):
        print("inser...")
        result = self.my_col.insert(dict)
        return result

    # 插入字典
    def InsertDictWithCollection(self, collection, dict):
        print("inser...")
        result = collection.insert(dict)
        return result

    # 插入字典列表
    def InsertDicts(self, list):
        print("inser...")
        result = self.my_col.insert_many(list)
        return result

    # 插入字典列表
    def InsertDictsWithCollection(self, collection, list):
        print("inser...")
        result = collection.insert_many(list)
        return result

    def Delete(self, dic):
        print("delete...")
        data = self.my_col.remove(dic)
        return data

    def Update(self, dic, newdic):
        print("update...")
        data = self.my_col.update(dic, newdic)
        return data

    # 根据条件查找
    # { "name": "RUNOOB" }
    def FindData(self, info):
        print("find...")
        result = self.my_col.find(info)
        return result

    def FindDataLimit(self, dic, number):
        print("find...")
        data = self.my_col.find(dic).limit(number)
        return data

    def FindDataSortL2B(self, dic, number, sortKey):
        print("find...")
        data = self.my_col.find(dic).sort(sortKey)
        return data

    def FindDataSortB2L(self, dic, number, sortKey):
        print("find...")
        data = self.my_col.find(dic).sort(sortKey, -1)
        return data

    # 根据条件查找
    def FindDataWithCollection(self, collection, info):
        print("find...")
        result = collection.find(info)
        return result

    # 查找指定字段
    # 我们可以使用 find() 方法来查询指定字段的数据，将要返回的字段对应值设置为 1。
    #{{},{ "_id": 0, "name": 1, "alexa": 1 }}
    # 除了 _id 你不能在一个对象中同时指定 0 和 1，如果你设置了一个字段为 0，则其他都为 1，反之亦然。
    def FindTargetValue(self, info):
        print("find...")
        result = self.my_col.find({}, info)
        return result

    # 查找指定字段
    def FindTargetValueWithCollection(self, collection, info):
        print("find...")
        result = collection.find({}, info)
        return result


#mongo = MyMongoDB()
# dic={"name":"zhangsan","age":18}
# find={"name":"zhangsan"}
# print(mongo.update(dic,{"name":"zhangsan","age":20}))
# print(mongo.InsertDict(dic))
# print(mongo.FindTargetValue({"urlToken":"lei-shen-fen"}))
# print(mongo.Update(dic,find))
# for x in mongo.Find({"userType": 0}):
#	print(x)
