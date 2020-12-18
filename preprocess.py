

import gen
import data
import csv
import os
import sys


# We could add additional profiles - children (various ages), pregnant women, etc.

class _Adult:
   DAILY = {
      data.VIT_B12   : 2.4,    # 2.4 mcg
      data.VIT_B6    : 1.3,    # 1.3 mg (19 – 50 years)
      data.VIT_C     : 65.0,   # daily 65 - 90 mg, and upper limit is 2000 mg
      data.VIT_E     : 15.0,   # 15 mg
      data.CALCIUM   : 1000.0, # 1000 mg (19 - 50 years)
      data.POTASSIUM : 3500.0  # 3500 – 4700 mg
   }
   
class AdultMale:
   FILE  = 'input/adult_male.csv'
   DAILY = {**_Adult.DAILY, **{
      data.VIT_A    : 2333.0, # 2333 IU, 700 mcg (18 years and older)
      data.VIT_K    : 138.0,  # 138 mcg
      data.IRON     : 19.3   # 19.3–20.5 mg
   }}
   
class AdultFemale:
   FILE  = 'input/adult_female.csv'
   DAILY = {**_Adult.DAILY, **{
      data.VIT_A    : 2000.0, # 2000 IU, 600 mcg (18 years and older)
      data.VIT_K    : 122.0,  # 122 mcg
      data.IRON     : 17.0    # 17.0 – 18.9 mg (over the age of 19)
   }}
   
class RealData:
   URL  = 'https://corgis-edu.github.io/corgis/csv/food/'
   FILE = 'input/corgis.csv'
   COLS = [
      "Description",
      "Data.Vitamins.Vitamin A - IU",
      "Data.Vitamins.Vitamin B12",     # mcg
      "Data.Vitamins.Vitamin B6",      # mg
      "Data.Vitamins.Vitamin C",       # mg
      "Data.Vitamins.Vitamin E",       # mg
      "Data.Vitamins.Vitamin K",       # mcg
      "Data.Major Minerals.Calcium",   # mg
      "Data.Major Minerals.Iron",      # mg 
      "Data.Major Minerals.Potassium", # mg
      "Data.Kilocalories"
   ]
   
   
def Read(fpath):
   """
      BRIEF  Read the csv file one row at a time
   """
   with open(fpath, 'r') as f:
      reader = csv.DictReader(f)
      for row in reader:
         yield [row[col] for col in RealData.COLS]
         
         
def Process(profile, rows):
   """
      BRIEF  Calculate percent daily values given one of the profile classes
             (e.g. AdultMale)
   """
   rows = list(rows)
   
   # First get the max value for the prop column
   max_prop = 0.0
   for row in rows:
      actual = float(row[data.PROP_COL_INDEX])
      if actual > max_prop:
         max_prop = actual
         
   for row in rows:
      processed = {data.NAME : row[data.NAME_COL_INDEX]}
      for i, nutrient in enumerate(data.NUTRIENTS):
         actual = float(row[i+1])
         target = profile.DAILY[nutrient]
         processed[nutrient] = data.PrettyString(actual/target if actual < target else 1.0)
      processed[data.PROPERTY] = data.PrettyString(float(row[data.PROP_COL_INDEX]) / max_prop)
      yield processed
      
      
def Main():
   """
      BRIEF  Generate input files from real world data
   """
   if not os.path.isfile(RealData.FILE):
      print('Missing required input: {0}'.format(RealData.FILE))
      print('Please download from:   {0}'.format(RealData.URL))
      sys.exit(1)
      
   for profile in [AdultMale, AdultFemale]:
      gen.Write(Process(profile, Read(RealData.FILE)), profile.FILE)
      
      
if __name__ == '__main__':
   """
      BRIEF  Main execution
   """
   Main()
   
   