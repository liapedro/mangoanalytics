# -*- coding: utf-8 -*-

#!/usr/bin/env python2.7
from __future__ import division
from asteriskMySQLManager import AsteriskMySQLManager
from assignCallCost import getStartOfDay, getEndOfDay
import datetime

class Digester:
	am = None

	def __init__(self):
		self.am = AsteriskMySQLManager()

	def getUserDailyDetail(self, day):
		callDetail = []	
		self.am.connect('nextor_tarificador')
		sql = "SELECT SUM(tarifica_call.cost) as cost, \
			SUM(tarifica_call.duration) as total_minutes, \
			COUNT(tarifica_call.id) as total_calls, \
			tarifica_extension.id as extension_number, \
			tarifica_call.date as date \
			FROM tarifica_call JOIN tarifica_extension \
			ON tarifica_call.extension_number = tarifica_extension.extension_number \
			WHERE date > %s AND date < %s \
			GROUP BY extension_number"
		self.am.cursor.execute(sql, (getStartOfDay(day), getEndOfDay(day)))
		for row in self.am.cursor.fetchall():
			callDetail.append((
				row['extension_number'],
				row['total_calls'],
				row['total_minutes'],
				row['cost'],
				row['date']
			))
		return callDetail

	def saveUserDailyDetail(self, day):
		callData = self.getUserDailyDetail(day)
		if len(callData[0]) == 0:
			print "No call information to save, ending..."
			return False

		self.am.connect('nextor_tarificador')
		sql = "INSERT INTO tarifica_userdailydetail \
		(extension_id, total_calls, total_minutes, cost, date) \
		VALUES(%s, %s, %s, %s, %s)"
		self.am.cursor.executemany(sql, callData)
		return self.am.db.commit()

	def getUserDestinationDetail(self, day):
		callDetail = []	
		self.am.connect('nextor_tarificador')
		sql = "SELECT SUM(tarifica_call.cost) as cost, \
			SUM(tarifica_call.duration) as total_minutes, \
			COUNT(tarifica_call.id) as total_calls, \
			tarifica_extension.id as extension_number, \
			tarifica_call.date as date, \
			tarifica_call.destination_group_id as destination_group \
			FROM tarifica_call JOIN tarifica_extension \
			ON tarifica_call.extension_number = tarifica_extension.extension_number \
			WHERE date > %s AND date < %s \
			GROUP BY destination_group_id"
		self.am.cursor.execute(sql, (getStartOfDay(day), getEndOfDay(day)))
		for row in self.am.cursor.fetchall():
			callDetail.append((
				row['extension_number'],
				row['total_calls'],
				row['total_minutes'],
				row['cost'],
				row['destination_group_id'],
				row['date']
			))
		return callDetail

	def saveUserDestinationDetail(self, day):
		callData = self.getUserDestinationDetail(day)
		if len(callData[0]) == 0:
			print "No call information to save, ending..."
			return False
		print len(callData[0])
		self.am.connect('nextor_tarificador')
		sql = "INSERT INTO tarifica_userdestinationdetail \
		(extension_id, total_calls, total_minutes, cost, destination_group_id, date) \
		VALUES(%s, %s, %s, %s, %s, %s)"
		self.am.cursor.executemany(sql, callData)
		return self.am.db.commit()

	def getUserDestinationNumberDetail(self, day):
		callDetail = []	
		self.am.connect('nextor_tarificador')
		sql = "SELECT SUM(tarifica_call.cost) as cost, \
			SUM(tarifica_call.duration) as total_minutes, \
			COUNT(tarifica_call.id) as total_calls, \
			tarifica_call.dialed_number as dialed_number, \
			tarifica_extension.id as extension_number, \
			DATE(tarifica_call.date) as date, \
			tarifica_destinationgroup.prefix as prefix \
			FROM tarifica_call LEFT JOIN tarifica_extension \
			ON tarifica_call.extension_number = tarifica_extension.extension_number \
			LEFT JOIN tarifica_destinationgroup \
			ON tarifica_call.destination_group_id = tarifica_destinationgroup.id \
			WHERE date > %s AND date < %s \
			GROUP BY tarifica_call.dialed_number"
		self.am.cursor.execute(sql, (getStartOfDay(day), getEndOfDay(day)))
		for row in self.am.cursor.fetchall():
			callDetail.append((
				row['extension_number'],
				row['total_calls'],
				row['total_minutes'],
				row['cost'],
				row['prefix'],
				row['dialed_number'],
				row['date']
			))
		return callDetail

	def saveUserDestinationNumberDetail(self, day):
		callData = self.getUserDestinationNumberDetail(day)
		print callData
		if len(callData[0]) == 0:
			print "No user destination number information to save, ending..."
			return False
		print len(callData[0])
		self.am.connect('nextor_tarificador')
		sql = "INSERT INTO tarifica_userdestinationnumberdetail \
		(extension_id, total_calls, total_minutes, cost, prefix, number, date) \
		VALUES(%s, %s, %s, %s, %s, %s, %s)"
		self.am.cursor.executemany(sql, callData)
		return self.am.db.commit()

	# -----------------TRUNKS---------------------
	def getProviderDailyDetail(self, day):
		callDetail = []	
		self.am.connect('nextor_tarificador')
		sql = "SELECT SUM(tarifica_call.cost) as cost, \
			SUM(tarifica_call.duration) as total_minutes, \
			COUNT(tarifica_call.id) as total_calls, \
			tarifica_call.date as date, \
			tarifica_destinationgroup.provider_id as provider \
			FROM tarifica_call JOIN tarifica_destinationgroup \
			ON tarifica_call.destination_group_id = tarifica_destinationgroup.id \
			WHERE date > %s AND date < %s \
			GROUP BY tarifica_destinationgroup.provider_id"
		self.am.cursor.execute(sql, (getStartOfDay(day), getEndOfDay(day)))
		for row in self.am.cursor.fetchall():
			callDetail.append((
				row['provider'],
				row['cost'],
				row['total_calls'],
				row['total_minutes'],
				row['date']
			))
		return callDetail

	def saveProviderDailyDetail(self, day):
		callData = self.getProviderDailyDetail(day)
		if len(callData[0]) == 0:
			print "No call information to save, ending..."
			return False

		self.am.connect('nextor_tarificador')
		sql = "INSERT INTO tarifica_providerdailydetail \
		(provider_id, cost, total_calls, total_minutes, date) \
		VALUES(%s, %s, %s, %s, %s)"
		self.am.cursor.executemany(sql, callData)
		return self.am.db.commit()

	def getProviderDestinationDetail(self, day):
		callDetail = []	
		self.am.connect('nextor_tarificador')
		sql = "SELECT SUM(tarifica_call.cost) as cost, \
			SUM(tarifica_call.duration) as total_minutes, \
			COUNT(tarifica_call.id) as total_calls, \
			tarifica_call.date as date, \
			tarifica_call.destination_group_id as destination_group_id, \
			tarifica_destinationgroup.provider_id as provider \
			FROM tarifica_call JOIN tarifica_destinationgroup \
			ON tarifica_call.destination_group_id = tarifica_destinationgroup.id \
			WHERE date > %s AND date < %s \
			GROUP BY tarifica_call.destination_group_id"
		self.am.cursor.execute(sql, (getStartOfDay(day), getEndOfDay(day)))
		for row in self.am.cursor.fetchall():
			callDetail.append((
				row['provider'],
				row['cost'],
				row['total_calls'],
				row['total_minutes'],
				row['destination_group_id'],
				row['date']
			))
		return callDetail

	def saveProviderDestinationDetail(self, day):
		callData = self.getProviderDestinationDetail(day)
		if len(callData[0]) == 0:
			print "No call information to save, ending..."
			return False
		print len(callData[0])
		self.am.connect('nextor_tarificador')
		sql = "INSERT INTO tarifica_providerdestinationdetail \
		(provider_id, cost, total_calls, total_minutes, destination_group_id, date) \
		VALUES(%s, %s, %s, %s, %s, %s)"
		self.am.cursor.executemany(sql, callData)
		return self.am.db.commit()



if __name__ == '__main__':
	week = datetime.datetime.now()
	week = week - datetime.timedelta(days=31)
	print week
	d = Digester()
	# d.saveUserDailyDetail(week)
	# d.saveUserDestinationNumberDetail(week)
	# d.saveProviderDailyDetail(week)
	d.saveProviderDestinationDetail(week)

