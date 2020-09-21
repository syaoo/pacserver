# here is some assistanat function
# create date: 2020.09.21
# author: syaoo


import leancloud, os
# add rules
def add_rule(TabName, rules):
    """
    This function is used to add items to a leancloud table.
    args:
        TabName - string, existing Leancloud datatable name, If the table does not exist, an error will occur;
        rules - list, dict, if is list only have rules, if is dict both rules and commit. e.g. ['rule1','rule2'] or {'rule1':'comment1','rule2':'comment2'}
    return:
        counter - a counter for saved items number.
    """
    Obj = leancloud.Object.extend(TabName)
    query = Obj.query
    counter = 0
    add_rules = []
    for r in rules:
        query.equal_to('rule',r)
        if len(query.find())==0:
            add_rules.append([])
            add_rules[counter] = Obj()
            add_rules[counter].set("rule",r)
            add_rules[counter].set('comment','commit')
            add_rules[counter].increment('id',1)
            counter += 1
    Obj.save_all(add_rules)
    return counter