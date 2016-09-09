'''
Anthony Karnati
5/2/14
CS110-A55
akarnat1@binghamton.edu
Assignment 13
'''

'''
This program finds the population of a city via database query
Output:
  query result (str)
Input:
  city (str)
Classes Used:
  BadArgument
  QueryWorldBD
'''

import sqlite3

# ---------------------------------------------------------------------
'''
User defined exception class (subclass of Exception)
Used to signal program that query should not be issued
'''

class BadArgument(Exception):
  
#-- Constructor --------------------------------------------------------
  
  def __init__(self):
    self.__title = 'Bad Argument'
    self.__message = 'Max/Min is blank or contains invalid characters'

#-- Accessors ----------------------------------------------------------
    
  # return title (str)
  def getTitle(self):
    return self.__title
    
#-- to String ----------------------------------------------------------
  
  def __str__(self):
    return self.__message

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------



'''
Encapsulates a  population query sent to world database
'''
class QueryWorldDB:
  
  # Connect to database and get cursor
  # param dbName (str)
  def __init__(self, dBName):
    conn = sqlite3.connect(dBName)
    self.__cursor = conn.cursor()
    # Must make city instance variable so that it is accessible to all methods
    self.__answer = None
    self.__minPop=''
    self.__maxPop=''
    

# -- Accessors ---------------------------------------------------------------

  def getAnswer(self):
    return self.__answer

# -- Predicate ---------------------------------------------------------------

  def isValidRange(self):
    return self.__maxPop>self.__minPop

# -- Mutators ----------------------------------------------------------------

  # param maxNum (str)
  def maxSearch(self,maxNum):
    self.__maxPop= maxNum

  # param minNum (str)
  def minSearch(self,minNum):
    self.__minPop= minNum
  
  

  # Note that if city isn't in database, then answer will be None
  # If city is in database, answer will be a tuple object
  # Will have to get element[0] of tuple in order to use it
  def setAnswer(self):
    self.__answer = self.__cursor.fetchall()

  # raises BadArgument Exception if city is blank or contains invalid chars
  def popQuery(self):
      self.__cursor.execute('select name,population from city where population>= ? and population <=? ',\
                          (self.__minPop, self.__maxPop))


  # Close connection to db
  def closeConnection(self):
    self.__cursor.close()

# -- toString ----------------------------------------------------------------

  # return result (str)
  def __str__(self):
    # Note that 4th format specifier denotes a string rather than an int in 
    # order to accommodate possibility that answer is None

    returnMe=''
    
    for tuples in self.__answer:

      firstPart=tuples[0]
      secondPart=tuples[1]
      
      returnMe+='City:'
      returnMe+= firstPart
      returnMe+='       Population:'
      returnMe+= str(secondPart)
      returnMe+= '\n'
    return returnMe


    '''%s %s %s %s\n' % (
    ('The population of' if self.__answer else 'There is no city named'),
    self.__currentCity,
    ('is' if self.__answer else 'in the database'),
    self.__answer )'''
  
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
 
# Find population of any city stored in world database
# Cities must contain only alphabetic characters with the exeception of mult-
#   word cities, which must be connected with '_' (no spaces allowed)
def main():
  # set up connection and create cursor
  query = QueryWorldDB('worldDB (2)')

  # get input from user (priming read)
  minPop = input("Find the cities with population within a range\n" + \
               "Enter the minimum population number or press <Enter> to quit):  ")
  while minPop:

    maxPop= input("Enter the maximum population number: ")


    query.maxSearch(maxPop)
    query.minSearch(minPop)
    
    try:
    # set up and issue query

      while not query.isValidRange():
        minPop= input("Invalid range. Reenter minimum: ")
        maxPop= input("Reenter maximum: ")
        
      query.minSearch(minPop)
      query.maxSearch(maxPop)                               
      
      query.popQuery()
      query.setAnswer()
      # show results
      print(query)
        
    except BadArgument as err:
      # max/min inputs are empty or malformed
      print('\n%s: %s\n' % (err.getTitle(), str(err) ))
       
    # let user enter another city (continuation read)
    minPop = input("Enter next population minimum.(Press <Enter> to quit):  ")
    
  # close connection to db
  query.closeConnection()

main()
