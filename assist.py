# here is some assistanat function
# create date: 2020.09.21
# author: syaoo


import leancloud, os
# add rules
def add_items(TabName, Items,Uniques=[]):
    """
    This function is used to add items to a leancloud table.
    Note: before use this function should init leancloud use `init()` function leancloud.init("appid", "appkey")
    args:
        TabName - string, existing Leancloud datatable name, If the table does not exist, an error will occur;
        items - dict or dict-list, if is list only have rules, if is dict both rules and commit. e.g. ['rule1','rule2'] or {'rule1':'comment1','rule2':'comment2'}
    return:
        counter - a counter for saved items number.
    """
    # check the type of Items
    if isinstance(Items, dict):
        Items = [Items]
    counter = 0
    all_item = []
    if isinstance(Items, list):
        # process all item in the list
        for item in Items:
            # 为 leancloud.Object 创建子类Obj
            Obj = leancloud.Object.extend(TabName)
            query = Obj.query
            checked = 0
            # check Unique keys
            for key in Uniques:
                if key  in item.keys():
                    query.equal_to(key,item[key])
                    res = query.find()
                    if len(res) > 0:
                        checked += 1
            if checked > 0 and checked == len(Uniques):
                # if all Unique keys' value is same use update this item;
                objectId = res[0].get('objectId')
                updateItem = Obj.create_without_data(objectId)
                all_item.append(updateItem)
                for key, val in item.items():
                    updateItem.set(key, val)
                counter += 1
            else:
                # if now add a new item;
                addItem = Obj() # 为Obj类创建一个新实例
                all_item.append(addItem)
                for key, val in item.items():
                    addItem.set(key,val)
                # addItem.save()
                counter += 1
            Obj.save_all(all_item)
    
    # Obj.save_all(add_rules)
    return 

if __name__ == "__main__":
    APPID = os.getenv('LC_APPID')
    APPKEY = os.getenv('LC_APPKEY')

    # init leancloud
    leancloud.init(APPID, APPKEY)
    tabname = 'test'
    items = [{'key1':'val11','key2':'val332'},{'key1':'val22','key2':'val22'}]
    add_items(tabname,items,['key1'])
