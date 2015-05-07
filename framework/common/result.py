"""
@authors: Sergei Garbuzov
@status: Development
@version: 1.0.0

status.py: TBD


"""

from framework.common.status import OperStatus
#from framework.common.status import OperStatus, STATUS
#from framework.controller.netconfnode import NetconfNode

class Result(object):
    """ TBD """
    def __init__(self, status=None, data=None):
        """Initializes this object properties."""
#        raise AttributeError('!!!+-+-+-+-')
        if isinstance(status, OperStatus) == False:
            raise TypeError(status)
        self.status = status
        self.data = data
    
    '''
    def set_status(self, status):
        if isinstance(status, OperStatus) == False:
            raise TypeError(status)
        self.status = status
    '''
    '''
    def set_data(self, data):
        self.data = data
    '''
    def get_status(self):
        assert (self.status != None)
        return self.status

    def get_data(self):
        return self.data

'''
if __name__ == "__main__":
        nlist = []  
        status = OperStatus()
        status.set_status(STATUS.CONN_ERROR)
        for i in range (3,8):
            nlist.append(i)
        
        result = Result(status, nlist)
        
        status = result.get_status()
        print status
        
        data = result.get_data()
        print data
'''

        