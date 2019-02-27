# Transaction.py
# This file handles all the transactions done from one account to another
#
#

import Utility as util
import Accounts as ac
import DBQuery as dbq
import TransactionOutput as TxOut

class Transaction:

	txcount = 0

	def __init__(self,giver,taker,output):		#output is of type TxOutputs
		self.value = 1
		self.sender = giver						#objects of one of classes in Accounts.py
		self.recept = taker						#objects of one of classes in Accounts.py
		self.txid = self.calcID()
		self.is_proc = False
		self.signature = None


	def __repr__(self):
		if self.is_proc == True:
			return (str(self.sender) + " gave " + str(self.recept) + " a vote!")
		else:
			return ("Transaction under process or not defined!")


	def calcID(self):									#Hashed transactionID (txid) to be given to TOuput
		Transaction.txcount += 1
		return util.applySHA256(self.sender.pk.to_string() + self.recept.to_string()+str(Transaction.txcount))

	def signTransaction(self):
		data = self.sender.pk.to_string() + self.recept.pk.to_string()
		self.signature = util.applySignature(self.sender.sk.to_string(),data)
		if self.signature == None:											#signing failed
			return False
		else:																#signed successfully
			print("The Transaction was signed successfully!")
			return True

	def processTransaction(self):
		data = self.sender.pk.to_string() + self.recept.pk.to_string()
		publicKey = dbq.getpublicKey(self.sender.name,self.sender.dob)
		if util.verifySignature(publicKey, data, self.signature):
			print("Tranasaction Signature Validated!")
			txoutput = TxOut.TxOutput(self.recept.pk.to_string(),self.txid)
			self.is_proc = True
		else:
			print("Transaction Signature Not Valid!")
			self.is_proc = False

		return self.is_proc


if __name__ == "__main__":
	v1 = ac.Voter(102,"Polly Robertson","2018-11-12")
	p1 = ac.Party(103,"BJP")
	tr1 = Transaction(v1,p1)
	tr1.signTransaction()	
	tr1.processTransaction()
	print(tr1.txid) 
	print(tr1.is_proc)
