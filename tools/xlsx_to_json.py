#!/usr/bin/env python3

from datetime import date
import json
import pandas
import sys

def process_attribute(blob, label, attribute):
  blob[label] = attribute

def process_location(labels, location, last):
  row = 0
  total_rows = len(labels.index) 
  location_blob = {"@type":"CovidTestingFacility"} 
  while row < total_rows:
    label = labels.iloc[row]
    attribute = location.iloc[row]
    if pandas.isnull(attribute):
      row += 1
      continue
    process_attribute(location_blob, label, attribute)
    row += 1
  return_string = json.dumps(location_blob)
  print(return_string)
  if not last:
    return_string += ","
  return return_string

def process_df(df):
  labels = df.iloc[:,1]
  locations = df.iloc[:,2:]
  today = date.today().strftime("%Y-%m-%d")
  # TODO take in url as an argument
  result = """
         {{
           "@context": "https://schema.org",
           "@type": "SpecialAnnouncment",
           "name": "COVID-19 Testing Facilities",
           "datePosted": "{}",
           "url": "",
           "announcmentLocation": [
         """.format(today)
  number_of_locations = len(locations.columns)
  location = 0
  last = False
  while location < number_of_locations:
    if (location+1)==number_of_locations:
      last = True 
    location_blob = process_location(labels, locations.iloc[:,location], last)
    result += location_blob
    location += 1
  result += """
            ]
          }"""
  print("<script type=\"application/ld+json\">")
  parsed = json.loads(result.strip())
  print(json.dumps(parsed, indent=4))
  print("</script>")

def main():
  if len(sys.argv) < 3:
    print("Arguments missing. Run `./xlsx_to_json filname sheetname.`")
    exit()
  filename = sys.argv[1]
  sheetname = sys.argv[2]
  df = pandas.read_excel(filename, sheet_name=sheetname)
  process_df(df)

if __name__ == "__main__":
  main()
