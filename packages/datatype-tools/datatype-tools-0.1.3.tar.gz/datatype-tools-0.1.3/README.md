# Data Type Tools
[![Build Status](https://travis-ci.org/edmundpf/datatype_tools.svg?branch=master)](https://travis-ci.org/edmundpf/datatype_tools)
[![PyPI version](https://badge.fury.io/py/datatype-tools.svg)](https://badge.fury.io/py/datatype-tools)
> Includes useful helper methods for Python's immutable data types using the *forbiddenfruit* library.
## Install
* `python3 -m pip install datatype-tools`
## Usage
* Import single datatype
	* `from datatype_tools.lib import Float`
* Import all datatypes
	* `from datatype_tools.lib import *`
## Dict Tools
* *sort_by_val*
	 * Sorts dictionary by values, expects dictionary with a depth of 1
		 ``` python
		 >>> obj = {'a': 3, 'b': 1, 'c': 2}
		 >>> obj.sort_by_val(sort_type='int')
		 {'b': 1, 'c': 2, 'a': 3}
		 ```
	* Arguments
		* *self*: dictionary
		* *asc*: boolean (True)
			* Ascending order when True, Descending when False
		* *sort_type*: string ('string')
			* Data Type for sort, includes 'string', 'int', 'float', and 'date' types
			* Date Type is a string representing a date
			* Data does not need to match type i.e. a string with an int value '1'
			* Returns original data type
		* *date_input*: string ('mdy')
			* Date input format
			* i.e. 'ymd', 'mdy', etc.
	* Returns sorted dict
* *sort_by_key*
	* Sorts dictionary by keys, expects dictionary with a depth of 1
		 ``` python
		 >>> obj = {'c': 1, 'a': 3, 'b': 2}
		 >>> obj.sort_by_key(sort_type='string')
		 {'a': 3, 'b': 2, 'c': 1}
		 ```	
	* Arguments
		* *self*: dictionary
		* *asc*: boolean (True)
			* Ascending order when True, Descending when False
		* *sort_type*: string ('string')
			* Data Type for sort, includes 'string', 'int', 'float', and 'date' types
			* Date Type is a string representing a date
			* Data does not need to match type i.e. a string with an int value '1'
			* Returns original data type
		* *date_input*: string ('mdy')
			* Date input format
			* i.e. 'ymd', 'mdy', etc.
	* Returns sorted dict
* *nested_sort*
	* Sorts dictionary by nested key value
		 ``` python
		 >>> obj = {'a': {'b': {'c': 2}}, 'b': {'b': {'c': 1}}}
		 >>> obj.nested_sort(nested_args=[{'keys': ['b', 'c'], 'sort_type': 'int'}])
		 {'b': {'b': {'c': 1}}, 'a': {'b': {'c': 2}}}
		 ```
	* Arguments
		* *self*: dictionary
		* *asc*: boolean (True)
			* Ascending order when True, Descending when False
		* *nested_args*: list
			* List of sort argument dicts, can include multiple to sort by multiple nested keys respectively
			* Args
				* *keys*: list
					* list of nested keys respectively i.e. ['b', 'c', 'd'] will sort by key ['b']['c']['d']
				* *sort_type*: string ('string')
					* Data Type for sort, includes 'string', 'int', 'float', and 'date' types
					* Date Type is a string representing a date
					* Data does not need to match type i.e. a string with an int value '1'
					* Returns original data type
				* *date_input*: string ('mdy')
					* Date input format
					* i.e. 'ymd', 'mdy', etc.
	* Returns sorted dict
## List Tools
* *sort_by_val*
	 * Sorts list of dictionaries by values, expects dictionaries with a depth of 1
		 ``` python
		 >>> li = [{'a': 3}, {'b': 1}, {'c': 2}]
		 >>> li.sort_by_val(sort_type='int')
		 [{'b': 1}, {'c': 2}, {'a': 3}]
		 ```
	* Arguments
		* *self*: list
		* *asc*: boolean (True)
			* Ascending order when True, Descending when False
		* *sort_type*: string ('string')
			* Data Type for sort, includes 'string', 'int', 'float', and 'date' types
			* Date Type is a string representing a date
			* Data does not need to match type i.e. a string with an int value '1'
			* Returns original data type
		* *date_input*: string ('mdy')
			* Date input format
			* i.e. 'ymd', 'mdy', etc.
	* Returns sorted list
* *sort_by_key*
	* Sorts list of dictionaries by keys, expects dictionaries with a depth of 1
		 ``` python
		 >>> li = [{'c': 1}, {'a': 3}, {'b': 2}]
		 >>> li.sort_by_key(sort_type='string')
		 [{'a': 3}, {'b': 2}, {'c': 1}]
		 ```	
	* Arguments
		* *self*: list
		* *asc*: boolean (True)
			* Ascending order when True, Descending when False
		* *sort_type*: string ('string')
			* Data Type for sort, includes 'string', 'int', 'float', and 'date' types
			* Date Type is a string representing a date
			* Data does not need to match type i.e. a string with an int value '1'
			* Returns original data type
		* *date_input*: string ('mdy')
			* Date input format
			* i.e. 'ymd', 'mdy', etc.
	* Returns sorted list
* *sort_by_key_val*
	* Sorts list of dictionaries by specific key value, expects dictionaries with a depth of 1
		 ``` python
		 >>> li = [{'a': 1, 'b': 2}, {'a': 2, 'b': 1}]
		 >>> li.sort_by_key_val(key='b', sort_type='string')
		 [{'a': 2, 'b': 1}, {'a': 1, 'b': 2}]
		 ```	
	* Arguments
		* *self*: list
		* *asc*: boolean (True)
			* Ascending order when True, Descending when False
		* *sort_type*: string ('string')
			* Data Type for sort, includes 'string', 'int', 'float', and 'date' types
			* Date Type is a string representing a date
			* Data does not need to match type i.e. a string with an int value '1'
			* Returns original data type
		* *date_input*: string ('mdy')
			* Date input format
			* i.e. 'ymd', 'mdy', etc.
	* Returns sorted list
* *nested_sort*
	* Sorts list of dictionaries by nested key value
		 ``` python
		 >>> li = [{'a': {'b': {'c': 2}}}, {'b': {'b': {'c': 1}}}]
		 >>> li.nested_sort(nested_args=[{'keys': ['b', 'c'], 'sort_type': 'int'}])
		 [{'b': {'b': {'c': 1}}}, {'a': {'b': {'c': 2}}}]
		 ```
	* Arguments
		* *self*: list
		* *asc*: boolean (True)
			* Ascending order when True, Descending when False
		* *nested_args*: list
			* List of sort argument dicts, can include multiple to sort by multiple nested keys respectively
			* Args
				* *keys*: list
					* list of nested keys respectively i.e. ['b', 'c', 'd'] will sort by key ['b']['c']['d']
				* *sort_type*: string ('string')
					* Data Type for sort, includes 'string', 'int', 'float', and 'date' types
					* Date Type is a string representing a date
					* Data does not need to match type i.e. a string with an int value '1'
					* Returns original data type
				* *date_input*: string ('mdy')
					* Date input format
					* i.e. 'ymd', 'mdy', etc.
	* Returns sorted list
## String Tools
* *replace_multiple*
	* Replace multiple substrings or characters in a string with their respective replacements
		``` python
		>>> 'The Apple is Red'.replace_multiple({'Apple': 'Grass', 'Red': 'Green'})
		'The Grass is Green'
		```
	* Arguments
		* *self*: string
		* *dictionary*: dict
			* dict keys are the values to replace, and key values will be their respective replacements in the string
	* Returns string with replacements
* *format_date*
	* Formats string representing date in multiple formats
		``` python
		>>> '1/01/75'.format_date(date_input='mdy', date_format='mmddyyyy', delimiter='-')
		'01-01-1975'
		```
	* Arguments
		* *self*: string
		* *date_input*: string ('mdy')
			* date input order, i.e. 'mdy' for month, day, year, and 'ymd' for year, month, day
		* *date_format* string ('mmddyy')
			* date output format, the number of each letter correspond to date digits, i.e. a date with 'mmddyyyy' will have 4 digits for year while a date with 'mmddyy' will only have 2 digits for year
		* delimiter: string ('')
			* delimiter for date output, i.e. '/' yields 01/01/2019
	* Returns formatted date string
* *find_nth*
	* Find nth occurence of substring in string
		``` python
		>>> 'apple picking'.find_nth('p', 3)
		11
		```
	* Arguments
		* *self*: string
		* *string*: string
			* substring to search in string
		* *n*: int
			* 1-based occurence number of substring to find in string.
	* Returns int index
* *b64_enc*
	* Base64 encode string
	``` python
	>>> 'plain_text'.b64_enc()
	'cGxhaW5fdGV4dA=='
	```
	* Arguments
		* *self*: string
	* Returns string
* *b64_dec*
	* Base64 decode string
	``` python
	>>> 'cGxhaW5fdGV4dA=='.b64_dec()
	'plain_text'
	```
	* Arguments
		* *self*: string
	* Returns string
* *get_iso_date*
	* Get ISO Date from string
	``` python
	>>> '2019-05-27T19:09:04.285211Z'.get_iso_date()
	{'date': '05/27/2019', 'time': '19:09:04', 'micros': '285211', 'date_and_time': '05/27/2019-19:09:04', 'full_date': '05/27/2019-19:09:04.285211'}
	```
	* Arguments
		* *self*: string
		* iso_format: string, ISO datetime format for strftime
		* date_format: string, date output format
		* delimiter: string, date output delimiter
	* Returns dict
## Float Tools
* *round*
	* Round value to n decimal places (scientific rounding, fixes python rounding errors)
		``` python
		>>> 4.055.round(2)
		4.06
		>>> 4.054(2)
		4.05
		```
	* Arguments
		* *self*: float
		* *places*: int (2)
			* Number of places to round to
	* Returns rounded float
