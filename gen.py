

import data
import csv
import os
import random


SUPERFOOD_FILE = 'output/superfood.csv'
INPUT_FILE = 'input/random.csv'
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
         
def Read(fpath, skip_header = True):
   """
      BRIEF  Read the csv file one row at a time
   """
   with open(fpath, 'r') as f:
      reader = csv.reader(f)
      if skip_header:
         next(reader)
      for row in reader:
         yield list(row)
         
         
def PrettyPrint(fpath):
   """
      BRIEF  Read the csv file and print the contents
   """
   data.PrettyPrint(*Read(fpath, False))
   
   
def Main():
   """
      BRIEF  Generate a random input file
   """
   Write(RandomData(NUM_ROWS), INPUT_FILE)
   
   
if __name__ == '__main__':
   """
      BRIEF  Main execution
   """
   Main()
   
   