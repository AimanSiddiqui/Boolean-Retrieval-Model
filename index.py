# importing the required libraries and modules
from PyQt5.QtWidgets import QApplication, QLabel
import sys
import matplotlib.pyplot as plt 
import array as arr
from PyQt5.QtWidgets import *
from nltk.stem import PorterStemmer
import re



ps = PorterStemmer()

TotalDocs=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,55]

#function to retrieve stopword list
def GetStopWords():
 f = open("Stopword-List.txt", "r")
 stopwords = f.read()
 stopwords =  stopwords.split("\n")
 stopwords =[x.strip() for x in stopwords if x.strip()]
 return stopwords

#function to retrieve queries from file
def GetQuery():
 f = open("Querry List.txt", "r")
 query = f.read()
 query = query.split("\n\n")
 for index in range(0, len(query)):
  query[index] = query[index].split("\n")
 # print(query[5][0])
 return query

#remove punctuations and spaces,etc
def Normalization(doc):
 doc=re.sub(r"(?<!\w)([A-Za-z])\.", r"\1", doc)
 doc = doc.replace('\'','') 
 doc = doc.replace('.',' ')
 doc = doc.replace(']',' ')
 doc = doc.replace('!',' ')
 doc = doc.replace('-',' ')
 doc = doc.replace(':',' ')
 doc = doc.replace(';',' ')
 doc = doc.replace('?',' ')
 doc = doc.replace(',',' ')
 doc = doc.replace('"',' ')
 doc = doc.replace('[',' ')
 doc = doc.replace('(',' ')
 doc = doc.replace(')',' ')

 doc = doc.lower()
 doc = doc.split(" ")
 doc =[x.strip() for x in doc if x.strip()]
 return doc

# a class which has doc IDs and an array of positions of the words in that docID
class PLObj:
   def __init__(self, docID, index):
     self.docID = docID
     self.position= []
     self.position.append(index)

   def AddPosition(self, index):
     self.position.append(index)

def GetDocuments(i):
 f = open("Trump Speechs/speech_" + str(i) + ".txt", "r")
 doc = f.read()
 doc = doc.split("\n")
 doc = doc[1]
 doc = Normalization(doc)
 # dictOfWords = { i : 5 for i in doc }
 # stopwords = GetStopWords()
 # for index in range(0, len(stopwords)):
 #  while stopwords[index] in doc:
 #   doc.remove(stopwords[index])
 for w in range(0,len(doc)):
  doc[w] = ps.stem(doc[w])
 return doc

def CheckDocPresence(wordlst, index):
 for x in wordlst:
   if x.docID == index:
    return True
 return False


# function to form Dictionary 
def FormDictionary():
 s=GetStopWords()
 for w in range(0,len(s)):
  s[w] = ps.stem(s[w])
  print(s[w])
 Dictionary = {
  
 }
 for j in range(0,56):
  doc= GetDocuments(j)
  docIndex=j
  for i in range(0, len(doc)):
   if not(doc[i] in s):
    if doc[i] in Dictionary:
     if CheckDocPresence(Dictionary[doc[i]],docIndex):
      wordlst = Dictionary[doc[i]]
      for x in wordlst:
        if x.docID == docIndex:
         x.AddPosition(i) 
     else:
      p1 = PLObj(docIndex,i)
      Dictionary[doc[i]].append(p1) 
     
    else:
     p1 = PLObj(docIndex,i)
     Dictionary[doc[i]] =[]
     Dictionary[doc[i]].append(p1) 

 return Dictionary

# function to print Dictionary
def PrintDictionary(Dictionary):
 f = open("Index.txt", 'w')
 f.close()
 f = open("Index.txt",'a')
 for x, y in Dictionary.items():
  for i in range(0,len(y)):
   print(x,"-> (",y[i].docID,") -> ", y[i].position)
   f.write(str(x)+"-> ("+str(y[i].docID)+") -> "+str(y[i].position))

# function to check if the query is boolean of not
def CheckIfBoolean(querry_array):
 if ('not' in querry_array) or ('or' in querry_array) or ('and' in querry_array) or ('NOT' in querry_array) or ('OR' in querry_array) or ('AND' in querry_array):
  return True
 else:
  return False

# map the queery results from the dictionary
def GetQuerryDocs(query, d ,i):
 answer = []
 docArray = []
 for j in d[query[i]]:
  docArray.append(j.docID)
 return docArray

# fucntion to perform query to querry matching; main function to perform the querries
def ParseQuery(index, query, d):
 answer = []
 answer2 = []
 if (CheckIfBoolean(query)):
   for w in range(0,len(query)):
    query[w] = ps.stem(query[w])
   
   i=0
   while i < len(query):
    if (query[i] == 'not'):
     i = i + 1
     a = False
     if query[i] != '(':
      docArray = GetQuerryDocs(query, d ,i)
     else:
      # print(query[i+1:len(query)-1])
      a = True
      docArray = ParseQuery(index,query[i + 1:len(query)-1],d)  
     for item in range(0,56):
      if not(item in docArray):
       answer.append(item)
     # print(query[i] ,"->" , answer)
     if a == True:
      i = len(query)

    elif (query[i] == 'and' and i > 0):
     FinalAnswer = []
     i = i + 1
     a = False
     if query[i] != '(':
      answer2 = GetQuerryDocs(query, d ,i)
     else:
      # print(query[i+1:len(query)-1])
      a = True
      answer2 = ParseQuery(index,query[i + 1:len(query)-1],d) 
     # print(query[i] ,"->" , answer2)
     for item in answer2:
      if item in answer:
       FinalAnswer.append(item)
     answer=FinalAnswer
     # print(answer)
     if a == True:
      i = len(query)

    elif (query[i] == 'or' and i > 0):
     i = i + 1
     a = False
     if query[i] != '(':
      answer2 = GetQuerryDocs(query, d ,i)
     else:
      # print(query[i+1:len(query)-1])
      a = True
      answer2 = ParseQuery(index,query[i + 1:len(query)-1],d) 
     # print(query[i] ,"->" , answer2)
     for item in answer2:
      if not(item in answer):
       answer.append(item)
     # print(answer)
     if a == True:
      i = len(query)

    else:
     answer = GetQuerryDocs(query, d ,i)
     # print(query[i] ,"->" , answer)

    i = i + 1
 if '/' in str(query) or (len(query)>1 and CheckIfBoolean(query)==False): #handling Proximity Querry
  # print("it is a proximity query!")
  answer = HandleProximityQ(index, query, d , 1)
 elif len(query) == 1:
  for w in range(0,len(query)):
   query[w] = ps.stem(query[w])
  answer = GetQuerryDocs(query, d ,0)
 return answer
    
#function to handle Proximity Queries
def HandleProximityQ(index, query, d, k ):
 postingLists = []
 answer = []
 for w in range(0,len(query)):
  query[w] = ps.stem(query[w])
 for item in query:
  if '/' in item:
   k = item[1]
   k = int(k) + 1
   # print(k)
 i = 0
 for item in query:
  if not('/' in item):
   docArray = []
   for j in d[item]:
    docArray.append(j)
   postingLists.append(docArray)
   i = i + 1
 i = 0
 while i < len(postingLists[0]):
  j = 0
  while j < len(postingLists[1]):
   if postingLists[0][i].docID == postingLists[1][j].docID:
    # print(postingLists[0][i].docID)
    answerBool = CheckPostionProximity(postingLists[0][i].position,postingLists[1][j].position,k)
    if answerBool : 
     answer.append(postingLists[1][j].docID)
   j = j + 1
  i = i + 1
 # print(answer)
 return answer

# function to check the positions and check if they exists in K distance
def CheckPostionProximity( P1 , P2 , k):
 
 i_count = 0
 j_count = 0
 while i_count < len(P1) and j_count < len(P2):
  if (P2[j_count] - P1[i_count] ) == k  :
   return True
  elif P2[j_count] <= P1[i_count]:
   j_count = j_count + 1
  else:
   i_count = i_count + 1
  
 return False
  



# settings for the GUI
app = QApplication([])
app.setStyle('Breeze')
window = QWidget()
layout = QVBoxLayout()
window.setStyleSheet("width: 1000px; background: #A1C7C4 ; ")
button = QPushButton('Search')
l1 = QLabel()
l1.setText("Select Query: (Please wait for a minute after pressing the search button and also do not get confused by a not responding message. The output will come in a while!) ")
layout.addWidget(l1)
layout.addStretch()
q = []
b2 = QButtonGroup()
query = GetQuery()
for i in range(0,24):
 q.append(QRadioButton(str(i) + " -> " + query[i][0]))
for i in range(0,24):
 b2.addButton(q[i]) 
for i in range(0,24):
 layout.addWidget(q[i])

# function for the action of the search button; it serves as main 
def on_button_clicked():
 #saving the dictionary of words in the documents and also indexing them through the following  function
 d=FormDictionary()
 PrintDictionary(d)
 query = GetQuery()
 for i in range(0,24):
  if q[i].isChecked() == True:
    option = i
    # print(option)
 querry_array = query[option][0]
 querry_array = querry_array.lower()
 querry_array = querry_array.replace('(',' ( ')
 querry_array = querry_array.replace(')',' ) ')
 querry_array = querry_array.split(" ")
 querry_array = [x.strip() for x in querry_array if x.strip()]
 
 #calling the Query matvhing function
 answer = ParseQuery(option,querry_array,d)

 alert = QMessageBox()
 alert.setText( "It is present in the following documents: \n" +str(answer))
 alert.exec_()




#making connections from GUI to the logic and adding the widgets
button.clicked.connect(on_button_clicked)
layout.addStretch()
layout.addWidget(button)
window.setLayout(layout)
window.show()
app.exec_()