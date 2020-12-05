

NAME = 'name'
NUTRIENTS = ['A', 'B', 'C', 'D', 'E', 'K', 'calcium', 'iodine', 'iron']
PROPERTY = 'calories'

ALL_COLS = [NAME] + NUTRIENTS + [PROPERTY]

NAME_COL_INDEX = 0
PROP_COL_INDEX = -1


def PrettyPrint(rows):
   """
      BRIEF  Pretty print the rows of values
   """
   rows = list(rows)
   
   for i, row in enumerate(rows):
      for j, col in enumerate(row):
         val = str(col)
         try:
            int(val)
         except ValueError:
            try:
               val = "{:.2f}".format(float(val))
            except ValueError:
               pass
         rows[i][j] = val
         
   width = [0]*len(rows[0])
   for row in rows:
      for i, col in enumerate(row):
         if len(col) > width[i]:
            width[i] = len(col)
            
   for row in rows:
      print('  '.join(('{0:<' + str(width[i]) + '}').format(col) for i, col in enumerate(row)))
      
      