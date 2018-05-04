import pickle
from pprint import pprint

choreo = {16: 'axel',
	34: 'flip',
	49: 'lutz',
	64: 'loop'}

# new_choreo = {}
# for x, y in choreo:
# 	new_choreo[y] = 'non_filler'

# choreo = new_choreo

# print(choreo)


file_Name = "testfile"
# open the file for writing
fileObject = open(file_Name,'wb') 

# this writes the object a to the
# file named 'testfile'
pickle.dump(choreo,fileObject)   

# here we close the fileObject
fileObject.close()
# # we open the file for reading
fileObject = open(file_Name,'r')  
# # load the object from the file into var b
b = pickle.load(fileObject)  
pprint(b)
# ['test value','test value 2','test value 3']
# a==b
# True