#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


import time





class DateTimeFormat(object):
	"""
	%a - The abbreviated weekday name (Sun)
	%A - The full weekday name (Sunday)
	%b - The abbreviated month name (Jan)
	%B - The full month name (January)
	%d - Day of the month (01..31)
	%e - Day of the month (1..31)
	%H - Hour of the day, 24-hour clock (00..23)
	%I - Hour of the day, 12-hour clock (01..12)
	%l - Hour of the day ()
	%j - Day of the year (001..366)
	%m - Month of the year (01..12)
	%M - Minute of the hour (00..59)
	%p - Meridian indicator (AM or PM)
	%S - Second of the minute (00..60)
	%w - Day of the week (Sunday is 0, 0..6)
	%y - Year without a century (00..99)
	%Y - Year with century
	%Z - Time zone name
	%% - Literal % character
	"""


class iso8601(DateTimeFormat):
	"""
	YYYY = four-digit year
	MM   = two-digit month (01=January, etc.)
	DD   = two-digit day of month (01 through 31)
	hh   = two digits of hour (00 through 23) (am/pm NOT allowed)
	mm   = two digits of minute (00 through 59)
	ss   = two digits of second (00 through 59)
	s    = one or more digits representing a decimal fraction of a second
	TZD  = time zone designator (Z or +hh:mm or -hh:mm)
	
	Year:
	  YYYY (eg 1997)
	Year and month:
	  YYYY-MM (eg 1997-07)
	Complete date:
	  YYYY-MM-DD (eg 1997-07-16)
	Complete date plus hours and minutes:
	  YYYY-MM-DDThh:mmTZD (eg 1997-07-16T19:20+01:00)
	Complete date plus hours, minutes and seconds:
	  YYYY-MM-DDThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00)
	Complete date plus hours, minutes, seconds and a decimal 
	fraction of a second:
	  YYYY-MM-DDThh:mm:ss.sTZD (eg 1997-07-16T19:20:30.45+01:00)
	"""
	self.fmt = {
		"y" : {
			'fmt': "YYYY", "eg": "1997", 
			"desc" : "Year"
		},
		"ym" : {
			'fmt': "YYYY-MM", "eg": "1997-07", 
			"desc": "Year and Month"
		},
		"ymd" : {
			'fmt': "YYYY-MM-DD", "eg": "1997-07-16", 
			"desc": "Complete date"
		},
		"ymdt" : {
			'fmt': "YYYY-MM-DDThh:mmTZD", "eg": "1997-07-16T19:20+01:00", 
			"desc": "Complete date plus hours and minutes"
		},
		"ymdtss" : {
			'fmt': "YYYY-MM-DDThh:mmTZD", 
			"eg": "eg 1997-07-16T19:20:30.45+01:00", 
			"desc": """
				Complete date plus hours, minutes, and seconds
				"""
		},
		"ymdtsss" : {
			'fmt': "YYYY-MM-DDThh:mmTZD", 
			"eg": "eg 1997-07-16T19:20:30.45+01:00", 
			"desc": """
				Complete date plus hours, minutes, seconds and a 
				decimal fraction of a second
				"""
		}
	}
	








