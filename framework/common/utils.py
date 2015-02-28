"""
utils.py: Helper utilities


"""
import sys
import time
import string
import yaml


def remove_empty_from_dict(d):
    if type(d) is dict:
        return dict((k, remove_empty_from_dict(v)) for k, v in d.iteritems() if v and remove_empty_from_dict(v))
    elif type(d) is list:
        return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
    else:
        return d

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
#                print "<<<<<<<<<<<<<<<"
#                print k
#                print key
#                print ">>>>>>>>>>>>>>>"
                if (k == key):
#                    print "##############################"
                    return i
    
    return None
    '''
    try:
        res = l.index(item)
        print "+++"
        print res
    except ValueError:
        print "---"
        pass
    '''
    
#    return res
    '''
    print "-------"
    for i in l:
        print i
        print type(i)
        print item
        print type(item)
        if (i == item):
            return item
    print "-------"
        
    return None
    '''




def replace_str_value_in_dict(d, old, new):
#    print "! type=%s %s" % (type(d), d)
    if type(d) is dict:
        return dict((k, replace_str_value_in_dict(v, old, new)) for k, v in d.iteritems() if v and replace_str_value_in_dict(v, old, new))
    elif type(d) is list:
        return [replace_str_value_in_dict(v, old, new) for v in d if v and replace_str_value_in_dict(v, old, new)]
    elif type(d) is unicode:
#        print "6.1 %s => %s ; %s" % (d, old, new)
        d = string.replace(d, unicode(old), unicode(new))
#        print "6.2 %s => %s ; %s" % (d, old, new)
        return d        
    elif type(d) is str:
#        print "777777777777"
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