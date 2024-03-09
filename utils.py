#Utility functions

#Self explanatory...
def writeBytesToFile(file,address,value,bytes):
	file.seek(address)
	file.write(value.to_bytes(bytes,'big'))