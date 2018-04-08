from ctypes import *

# Define some symbols
SQLITE_DELETE =  9
SQLITE_INSERT = 18
SQLITE_UPDATE = 23

# Define our callback function
#
# 'user_data' will be the third param passed to sqlite3_update_hook
# 'operation' will be one of: SQLITE_DELETE, SQLITE_INSERT, or SQLITE_UPDATE
# 'db name' will be the name of the affected database
# 'table_name' will be the name of the affected table
# 'row_id' will be the ID of the affected row
def callback(user_data, operation, db_name, table_name, row_id):
    if operation == SQLITE_DELETE:
        optext = 'Deleted row'
    elif operation == SQLITE_INSERT:
        optext = 'Inserted row'
    elif operation == SQLITE_UPDATE:
        optext = 'Updated row'
    else:
        optext = 'Unknown operation on row'
    s = '%s %ld of table "%s" in database "%s"' % (optext, row_id, table_name, db_name)
    print s

# Translate into a ctypes callback
c_callback = CFUNCTYPE(c_void_p, c_void_p, c_int, c_char_p, c_char_p, c_int64)(callback)

# Load sqlite3
dll = CDLL('libsqlite3.so.0')

# Holds a pointer to the database connection
db = c_void_p()

# Open a connection to 'test.db'
dll.sqlite3_open('test.db', byref(db))

# Register callback
dll.sqlite3_update_hook(db, c_callback, None)

# Create a variable to hold error messages
err = c_char_p()

# Now execute some SQL
dll.sqlite3_exec(db, 'create table foo (id int, name varchar(255))', None, None, byref(err))
if err:
    print err.value
dll.sqlite3_exec(db, 'insert into foo values (1, "Bob")', None, None, byref(err))
if err:
    print err.value
