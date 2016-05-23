#!env/bin/python
"""	DBManager.py Module allow databse access
	Typical insert statements and select statements
	No complicated queries as our system does not require it
	It also updates the DataStructures used to check whether the thresholds of conditions/parameters/faults/counters have been exceeded
	The actual checking is done else where
	Alerts are inserted after confirmation from server has been received
"""

import sys
import time
import sqlite3 as lite

con = None
cur = None

def InsertCustomer(_customerDict):
	"""
		Inserts parameter into the log table 
		Is to be called only id the parameter value does not match the current value

		Returns a list with [True] if everything goes off well
		Otherwise returns a list [False, Issue With insertion]

	"""
	global con
	global cur
	_ret = []
	GetCursor()
        _insert_list = []
        if 'customerName' in _customerDict:
            _insert_list.append(_customerDict['customerName'].strip())
        else: 
            insert_list.append('Unknown Customer')
        if 'streetAddress' in _customerDict:
            _insert_list.append(_customerDict['streetAddress'].strip())
        else:
            _insert_list.append('')
        _insert_list.append('')#address_line2
        _insert_list.append('')#address_line3
        if '_area' in _customerDict:
            _insert_list.append(_customerDict['_area'].strip())
        else:
            _insert_list.append('')
        if 'postalCode' in _customerDict:
            _insert_list.append(_customerDict['postalCode'].strip())
        else:
            _insert_list.append('')
        if '_city' in _customerDict:
            _insert_list.append(_customerDict['_city'].strip())
        else:
            _insert_list.append('')
        _insert_list.append('')#state
	try:
            _insert = tuple(_insert_list)
            cur.execute('INSERT INTO leads (customer_name,address_line1, address_line2, address_line3, area_name, pincode, city, state )VALUES (?,?,?,?,?,?,?,?)',_insert)
            con.commit()
            _ret = [True]
	except Exception, err:
		sys.stderr.write('error operation...')
		print 'Error', err
		con.rollback()
		_ret = [False, err]
	finally:
		if con:
			con.close()
	return _ret






#INCREMENT COUNTER BY VALUE
def UpdateCounter(_counter,_value=10):
	"""
		Inserts counter increment into the log file
		Is to be called only id the counter value needs to be increments by a minimum value (>10)
		Also updates the current counter value which will be used to verify if current counter status is within the max value 

		Returns a list with [True] if everything goes off well
		Otherwise returns a list [False, Issue With insertion]

	"""
	global con
	global cur
	_ret = []
	print 'Updating counter...',_counter,_value
	GetCursor()
	try:
		#INSERT INTO COUNTER LOG
		_insert = (_counter,_value)
		cur.execute('INSERT INTO counterlog(counter_no,times)VALUES (?,?)',_insert)
		con.commit()
		#GET THE CURRENT VALUE OF COUNTER AND UPDATE IT WITH THE NEW VALUE
		CounterStatus[_counter] = CounterStatus[_counter] + _value
		_insert = (_value, _counter)
		cur.execute('UPDATE countermaster set current_value = current_value + ? WHERE counter_no = ?',_insert)
		con.commit()
		_ret = [True]
	except Exception, err:
		sys.stderr.write('error in operation...')
		print 'Error', err
		con.rollback()
		_ret = [False, err]
	finally:
		if con:
			con.close()
	return _ret

#RESET THE COUNTER TO ZERO AND RESET DATE TO CURRENT DATE
def ResetCounter(_counter):
	"""
		Resets the counter to zero
		Should be called only when the Service Engineer has replaced a spare

		Returns a list with [True] if everything goes off well
		Otherwise returns a list [False, Issue With insertion]

	"""
	global con
	global cur
	_ret = []
	print 'resetting counter...',_counter
	GetCursor()
	try:
		cur.execute('UPDATE countermaster set current_value = 0 , reset_date = CURRENT_DATE  WHERE counter_no = ?',(_counter,))
		con.commit()
		CounterStatus[_counter] = 0
		_ret = [True]
	except Exception, err:
		sys.stderr.write('error in operation...')
		print 'Error', err
		con.rollback()
		_ret = [False,err]
	finally:
		if con:
			con.close()
	return _ret


def GetQueryResults(_query):
	"""
		Accepts a query as a string - simple select statement
		returns a tuple/list with each element as as a row
		each row is a dictonary with key as column name and value as the value of that collumn
		returns None if there is any issue

	"""
	global con
	global cur
	print 'retreiving from...', _query
	GetCursor()
	_arr = None
	try:
		cur.execute('PRAGMA foreign_keys = ON;')
		cur.execute(_query)
		_arr = cur.fetchall()		
	except Exception, err:
		print 'Error: ', err
	finally:
		if con:
			con.close()
	return _arr

def GetTable(_table_name):
	"""
		Accepts a tablename and returns all the rows from that table
		Select * from tablename
	"""
	_query = 'SELECT * FROM ' + _table_name
	return GetQueryResults(_query)



def GetCursor():
	"""
		Sets global cursor anc connection variables
		Returns True if no exception occurs else returns  False
	"""
	global con
	global cur
	con = None
	cur = None
	try:
		con = lite.connect('customer_list.db', detect_types=lite.PARSE_DECLTYPES)
		cur = con.cursor()
		cur.execute('PRAGMA foreign_keys = ON;')
		return True
	except Exception, err:
		print 'Error: ', err
		return False
	

if  __name__ == '__main__':
	print 'DbManager Works...'
