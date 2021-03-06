

import sys


NAME      = 'name'
VIT_A     = 'A'
VIT_B12   = 'B12'
VIT_B6    = 'B6'
VIT_C     = 'C'
VIT_E     = 'E'
VIT_K     = 'K'
CALCIUM   = 'calcium'
IRON      = 'iron'
POTASSIUM = 'potassium'
NUTRIENTS = [VIT_A, VIT_B12, VIT_B6, VIT_C, VIT_E, VIT_K, CALCIUM, IRON, POTASSIUM]
PROPERTY = 'calories'

ALL_COLS = [NAME] + NUTRIENTS + [PROPERTY]

NAME_COL_INDEX = 0
PROP_COL_INDEX = -1


def PrintBanner(delim, msg):
   """
      BRIEF  Print a message in between two 'delim' lines.
             If delim is an empty string, the two lines will be empty.
   """
   print('{0}\n{1}\n{0}'.format(delim*80, msg))
   sys.stdout.flush()
   
   
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
         
   sys.stdout.flush()
   
   
def PrettyString(val):
   """
      BRIEF  If it's a float, reduce to 2 digits
   """
   if isinstance(val, list) or isinstance(val, tuple):
      return "({0})".format(', '.join([PrettyString(item) for item in val]))
   elif callable(val):
      return val.__name__
   else:
      val = str(val)
      try:
         int(val)
      except ValueError:
         try:
            val = "{:.2f}".format(float(val))
         except ValueError:
            pass
      return val
      
      