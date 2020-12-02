

import data
import csv
import os
import random


INPUT_FILE = 'input/food.csv'
NUM_ROWS = 100000
PRECISION = 100


def RandomData(n_rows):
   """
      BRIEF  Generate random data
   """
   n_digits = len(str(n_rows-1))
   for i in range(n_rows):
      row = { data.NAME : 'food' + str(i).zfill(n_digits) }
      for nutrient in (data.NUTRIENTS + [data.PROPERTY]):
         row[nutrient] = random.randint(0,PRECISION)/PRECISION
      yield row
      
def Write(rows, fpath):
   """
      BRIEF  Write a csv file with random data
   """
   os.makedirs(os.path.dirname(fpath), exist_ok=True)
   with open(fpath, 'w', newline='') as f:
      writer = csv.DictWriter(f, data.ALL_COLS)
      writer.writeheader()
      for row in rows:
         writer.writerow(row)
         
def Read(fpath):
   """
      BRIEF  Read the csv file one row at a time
   """
   with open(fpath, 'r') as f:
      reader = csv.reader(f)
      next(reader) # skip header row
      for row in reader:
         yield list(row)
         
         
def PrettyPrint(fpath, header_msg):
   """
      BRIEF  Read the csv file and print the contents
   """
   rows = []
   with open(fpath, 'r') as f:
      reader = csv.reader(f)
      for row in reader:
         rows.append(row)
         
   width = [0]*len(rows[0])
   for row in rows:
      for i, col in enumerate(row):
         if len(col) > width[i]:
            width[i] = len(col)
            
   print('\n{0}\n'.format(header_msg))
   for row in rows:
      print('  '.join(('{0:<' + str(width[i]) + '}').format(col) for i, col in enumerate(row)))
      
      
if __name__ == '__main__':
   """
      BRIEF  Main execution - Generate a random input file
   """
   Write(RandomData(NUM_ROWS), INPUT_FILE)
   
   