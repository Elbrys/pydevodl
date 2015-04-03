"""
utils.py: Helper utilities


"""
import sys
import time
import string
import yaml

debug_count = 0

def remove_empty_from_dict(d):
    if type(d) is dict:
        return dict((k, remove_empty_from_dict(v)) for k, v in d.iteritems() if v and remove_empty_from_dict(v))
#        return dict((k, v) for k, v in d.iteritems() if v and remove_empty_from_dict(v))
    elif type(d) is list:
        return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
#        return [v for v in d if v and remove_empty_from_dict(v)]
    else:
        return d


def stripNone(data):
#    print "0)data=%s" % data
    if isinstance(data, dict):
#        print "1)data=%s" % data
        res = {k:stripNone(v) for k, v in data.items() if k != None and v != None}
#        print "1.1)res=%s" % res
        return res
#        return {k:stripNone(v) for k, v in data.items() if k != None and v != None}
    elif isinstance(data, list):
#        print "2)data=%s" % data
        res = [stripNone(item) for item in data if item != None]
#        print "2.1)res=%s" % res
        return res
#        return [stripNone(item) for item in data if item != None]
    elif isinstance(data, tuple):
#        print "3)data=%s" % data
        res = tuple(stripNone(item) for item in data if item != None)
#        print "3.1)res=%s" % res
        return res
#        return tuple(stripNone(item) for item in data if item != None)
    elif isinstance(data, set):
#        print "4)data=%s" % data
        res = {stripNone(item) for item in data if item != None}
#        print "4.1)res=%s" % res
        return res
#        return {stripNone(item) for item in data if item != None}
    else:
#        print "5)data=%s" % data
        return data














'''
def debugkv(k, v):
    print "<<<<<<"
    print ("k=%s, v=%s" % (k, v))
    if v == None:
        print ("None: k=%s, v=%s" % (k, v))
        print ">>>>>>"
        return False
    else:
        print ">>>>>>"
        return True
def debugv(v):
    print "<<<<<<"
    print ("k=NA, v=%s" % (v))
    print ">>>>>>"
    if v == None:
        return False
    else:
        return True
'''

'''
def remove_unset_values_from_nested_dict(d):
    if type(d) is dict:
        return dict((k, remove_unset_values_from_nested_dict(v)) for k, v in d.iteritems() if debugkv(k,v) and remove_unset_values_from_nested_dict(v))
#        return dict((k, v) for k, v in d.iteritems() if v and remove_empty_from_dict(v))
    elif type(d) is list:
        return [remove_unset_values_from_nested_dict(v) for v in d if debugv(v) and remove_unset_values_from_nested_dict(v)]
#        return [v for v in d if v and remove_empty_from_dict(v)]
    else:
        return d
'''



''' Keep!!!
def remove_unset_values_from_nested_dict(d):
    global debug_count
    res = {}
    debug_count +=1
    print ("1) +++ count=%d, res=%s" % (debug_count, d))
    for k, v in d.iteritems():
        print ("2) +++ k=%s,v=%s" % (k,v))
        if isinstance(v, dict):
            r1 = remove_unset_values_from_nested_dict(v)
            res[k] = r1
        elif v != None:
            res[k] = v
    
    return res
'''

'''
    print "<<<<<<<"
    print  d
    print ">>>>>>>"
    if type(d) is dict:
        res = {}
        for k, v in d.iteritems():
            print ("2) +++ k=%s, v=%s" % (k,v))
            if (v != None):
                res[k] = v
            remove_unset_values_from_dict(k)                    
        print ("3) +++ res=%s" % res)
        return res
    elif type(d) is list:
        res = []
        for v in d:
            if (v != None):
                res.append(v)
                remove_unset_values_from_dict(v)
        return res
    else:
        print ("4) +++ res=%s" % d)
        return d
'''

'''
def remove_unset_values_from_dict(d):
    print "///////////////////////////////"
    print d
    print "///////////////////////////////"
    if type(d) is dict:
        d1 = {}
        for k, v in d.iteritems():
#            print type(v)
            print "ahhha!!!!" if v == None else False
            print ("t=%s, k=%s, v=%s" % (type(v), k,v))
#            print v
            res = False
            if v != None:
                a1 = remove_empty_from_dict(v)
                print "a1=%s" % a1
                if a1 != None:
                    res = True
            print "res=%s" % res
            if res:
                print "++++++++++++++++"
                print v
                print "++++++++++++++++"
#                d1[k] = remove_empty_from_dict(v)
                d1[k] = v
        return d1
#                return dict((k, remove_empty_from_dict(v)))
#        return dict((k, remove_empty_from_dict(v)) for k, v in d.iteritems() if v and remove_empty_from_dict(v))
    elif type(d) is list:
        print "IIIIIIIIIIIIIIIIIII"
        return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
    else:
        print "<<<<<<<<<<<<<<<<<<<"
        print d
        print ">>>>>>>>>>>>>>>>>>>"
        return d
'''


def load_dict_from_file(f, d):
    try:
        with open(f, 'r') as f:
            obj = yaml.load(f)
        for k, v in obj.iteritems():
            d[k] = v
        return True
    except IOError:
        print("Error: failed to read file '%s'" % f)
        return False

def find_key_values_in_dict(d, key):
    """
    Searches a dictionary (with nested lists and dictionaries)
    for all the values matching to the provided key.
    """
    values = []

    for k, v in d.iteritems():
        if k == key:
            values.append(v)
        elif isinstance(v, dict):
            results = find_key_values_in_dict(v, key)
            for result in results:
                values.append(result)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    more_results = find_key_values_in_dict(item, key)
                    for another_result in more_results:
                        values.append(another_result)
    
    return values

def find_key_value_in_dict(d, key):
    """
    Searches a dictionary (with nested lists and dictionaries)
    for the first value matching to the provided key.
    """
    for k, v in d.iteritems():
        if k == key:
            return v
        elif isinstance(v, dict):
            results = find_key_values_in_dict(v, key)
            for result in results:
                return result
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    more_results = find_key_values_in_dict(item, key)
                    for another_result in more_results:
                        return another_result
    
    return None

def find_dict_in_list(l, key):
    for i in l:
        if (type(i) is dict):
            for k, v in i.items():
                if (k == key):
                    return i
    
    return None

def replace_str_value_in_dict(d, old, new):
    if type(d) is dict:
        return dict((k, replace_str_value_in_dict(v, old, new)) for k, v in d.iteritems() if v and replace_str_value_in_dict(v, old, new))
    elif type(d) is list:
        return [replace_str_value_in_dict(v, old, new) for v in d if v and replace_str_value_in_dict(v, old, new)]
    elif type(d) is unicode:
        d = string.replace(d, unicode(old), unicode(new))
        return d        
    elif type(d) is str:
        d = string.replace(d, old, new)
        return d
    else:
        return d    

def progress_wait_secs(msg=None, waitTime=None, sym="."):
    if (waitTime != None):
#        sys.stdout.write ("(waiting for %s seconds) " % waitTime)
#        sys.stdout.write ("waiting for %s seconds: " % waitTime)
#        sys.stdout.write ("waiting for %s seconds: " % waitTime)
        if (msg != None):
            sys.stdout.write ("%s" % msg)
        for i in range(0, waitTime, 1):
            print "%s" % sym, # <- no newline
            sys.stdout.flush() #<- makes python print it anyway
            time.sleep(1)
        sys.stdout.write ("\n")

'''        
def replace_underscores_with_dashes_in_dict(d):
    d1 = {}
    for k, v in d.iteritems():
        print type(k)
        if (type(k) is str):
            print "1)******"
            k1 = k.replace('_', '-')
        else:
            k1 = k
        
        print type(v)
        if (type(v) is str):
            print "1)******"
            v1 = v.replace('_','-')
        else:
            v1 = v
            
        d1[k1] = v1

    return d1
'''
