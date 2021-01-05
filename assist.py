# here is some assistanat function
# create date: 2020.09.21
# add class LcHandler: 2021.1.4
# author: syaoo


import leancloud, os, sys
# add rules
class LcHandler:
    """
    leancloud process class
    method:
    """
    def __init__(self,class_name):
        self.LC_class = leancloud.Object.extend(class_name)
        self.query=self.LC_class.query
        self.entry=self.LC_class()
        # self.entry.save()
    # query item

    def item_query(self, key_str,val):
        query=self.query
        try :
            query.equal_to(key_str,val)
            return query.find()
        except leancloud.LeanCloudError as e:
            if e.code == 101:
                return 0
            else:
                raise e
        
    # add items
    # def item_add(self, key_str,val):
    #     counter=0
    #     entry=self.entry
    #     res = self.item_query(key_str,val)
    #     if (res == 0 or len(res) == 0 ):
    #         entry.set(key_str,val)
    #         entry.save()
    #         counter+=1
    #     return counter

    def items_add(self, items,pkey=None):
        """
        This function is used to add items to a leancloud table.
        Note: before use this function should init leancloud use `init()` function leancloud.init("appid", "appkey")
        args:
            TabName - string, existing Leancloud datatable name, If the table does not exist, an error will occur;
            items - dict or dict-list, if is list only have rules, if is dict both rules and commit. e.g. ['rule1','rule2'] or {'rule1':'comment1','rule2':'comment2'}
        return:
            counter - a counter for saved items number.
        """
        # check the type of items
        if isinstance(items, dict):
            items = [items]
        counter = 0
        all_item = []
        if isinstance(items, list):
            # process all item in the list
            for item in items:
                if pkey:
                    res = self.item_query(pkey,item[pkey])
                else:
                    res = 0
                if (res==0 or len(res) == 0):
                    entry = self.LC_class()
                    # if lc class not exist or not find this item, add it
                    for k, v in item.items():
                        entry.set(k,v)
                    all_item.append(entry)
                else:
                    # if this item exist, update it
                    objid = res[0].get('objectId')
                    entry = self.LC_class.create_without_data(objid)
                    for key, val in item.items():
                        entry.set(key,val)
                    all_item.append(entry)
        counter = len(all_item)
        if counter > 0:
            self.LC_class.save_all(all_item)
        # Obj.save_all(add_rules)
        return  counter
        
    # delete one item
    def item_del(self,ObjID):
        """
        delete item use objectID
        """
        if isinstance(ObjID,str):
            ObjID=[ObjID]
        if isinstance(ObjID,list):
            for i in ObjID:
                entry = self.LC_class.create_without_data(i)
                entry.destroy()


if __name__ == "__main__":
    APPID = os.getenv('LC_APPID')
    APPKEY = os.getenv('LC_APPKEY')

    # init leancloud
    if (APPID == None or APPKEY == None):
        print("no 'LC_APPID' and 'LC_APPKEY' set.")
        sys.exit(0)
    leancloud.init(APPID, APPKEY)
    cname = 'test'
    items = [{'key1':'val11','key2':'val12'},{'key1':'val12','key2':'val22'}]
    lc=LcHandler(cname)
    lc.add_items(items,'key1')
    res = lc.item_query('key1','val11')
    print("{} matches.".format(len(res)))
    if len(res) > 0:
        oid=res[0].get('objectId')
        print("Object id is:<{}>".format(oid))
        # lc.item_del(oid)
