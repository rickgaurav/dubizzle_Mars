import os
import simplejson
import shutil


class Mars(object):
    """
    Class represnts Mars objects
    """

    def __init__(self, data_location=None):
        """
        Initialize Mars objects

        @param data_location:           Path to the data directory to be used to load and dump the objects
        @type data_location:            String
        """
        if data_location is None:
            self._data_location = os.path.join(os.path.dirname(__file__), 'data')
            if not os.path.exists(self._data_location):
                os.mkdir(self._data_location)
        elif not os.path.exists(data_location):
            raise RuntimeError("Data dir {0} does not exist".format(data_location))
        else:
            self._data_location = data_location
        self._data_file_path = os.path.join(self._data_location, 'data.txt')

    def send(self, data):
        """
        (over)writes a JSON object to a file. Takes in one argument of type
          dict. Returns 1 on success. Raises a general exception on error.

        @param data:                    Data as dictionary
        @type data:                     Dictionary

        @return:                        1 on success
        """
        try:
            simplejson.dump(data, open(self._data_file_path, 'wb'))
        except Exception, ex:
            raise RuntimeError('Failed to send object to the store. Reason {0}'.format(str(ex)))
        return 1

    def receive(self):
        """
        Reads a JSON object from a file. Returns a dict on success.
        Raises a general exception on error.

        @return: Dictonary representing the data
        """
        try:
            return simplejson.load(open(self._data_file_path, 'rb'))
        except Exception, ex:
            raise RuntimeError('Failed to read object from the store. Reason {0}'.format(str(ex)))


def test():
    """
    Test function to test reading and writing from/to file.
    """
    data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

    print "===================================================================="
    print "Case 1: When data directory exists and file can be read from as well as written into:"
    mars = Mars()
    print '\n\nWriting data {0} to File'.format(data)
    if mars.send(data) == 1:
        print 'Data is written to File'

    print '\n\nReading data from File'
    data = mars.receive()
    print 'Received the following data from the store: {0}'.format(data)
    print "===================================================================="

    print "\n\n\n===================================================================="
    print "\n Case 2: THE DATA DIRECTORY EXIST BUT CANNOT BE WRITTEN INTO: Should raise an exception"
    mars = Mars()
    file_dir = os.path.join(os.path.dirname(__file__), 'data')
    # Delete the dir `data` so that it raises an exception while writing to file
    shutil.rmtree(file_dir)
    mars.send(data)

if __name__ == '__main__':
    test() 