

NAME = 'name'
NUTRIENTS = ['A', 'B', 'C', 'D', 'E', 'K', 'calcium', 'iodine', 'iron']
PROPERTY = 'calories'

ALL_COLS = [NAME] + NUTRIENTS + [PROPERTY]

NAME_COL_INDEX = 0
PROP_COL_INDEX = -1


def PrintBanner(msg, delim = ''):
   """
      BRIEF  Print a banner with 
   """
   print('{0}\n{1}\n{0}'.format(delim*80, msg))
   
   
def PrettyPrint(*rows):
   """
      BRIEF  Pretty print the rows of values
   """
   if isinstance(rows[0], list):
      
      for i, row in enumerate(rows):
         for j, col in enumerate(row):
            rows[i][j] = PrettyString(col)
            
      width = [0]*len(rows[0])
      for row in rows:
         for i, col in enumerate(row):
            if len(col) > width[i]:
               width[i] = len(col)
               
      for row in rows:
         print('  '.join(('{0:<' + str(width[i]) + '}').format(col) for i, col in enumerate(row)))
         
   else:
      for row in rows:
         print(PrettyString(row))
         
         
def PrettyString(val):
   """
      BRIEF  If it's a float, reduce to 2 digits
   """
   val = str(val)
   try:
      int(val)
   except ValueError:
      try:
         val = "{:.2f}".format(float(val))
      except ValueError:
         pass
   return val
   
   