#!/usr/bin/env python3

from datetime import date
import json
import pandas
import sys

def process_attribute(blob, label, attribute):
  if "Name" == label: 
    blob["name"] = attribute
#  elif "Unique ID" == label:
  elif "Address Line 1" == label:
    blob["address"] = str(attribute)
  elif "Address Line 2" == label:
    blob["address"] += ", "
    blob["address"] += str(attribute)
  elif "City or Locality" == label:
    blob["address"] += ", "
    blob["address"] += str(attribute)
  elif "State or Province" == label:
    blob["address"] += ", "
    blob["address"] += str(attribute)
  elif "Postal Code" == label:
    blob["address"] += ", "
    blob["address"] += str(attribute)
  elif "COVID-19 testing website" == label:
    blob["url"] = str(attribute)
#  elif "Free COVID-19 tests" == label:
#  elif "Phone" == label:
#  elif "Email" == label:
#  elif "Website" == label:
#  elif "Category" == label:
#  elif "Latitude" == label:
#  elif "Longitude" == label:
#  elif "Monday" == label:
#  elif "Tuesday" == label:
#  elif "Wednesday" == label:
#  elif "Thursday" == label:
#  elif "Friday" == label:
#  elif "Saturday" == label:
#  elif "Sunday" == label:
#  elif "Appointment required" == label:
#  elif "Referral required" == label:
#  elif "Patient restrictions" == label:
#  elif "Location instructions" == label:
#  elif "Insurance accepted" == label:
#  elif "Insurance required" == label:
#  elif "Minimum age" == label:
#  elif "Languages spoken at location" == label:
#  elif "Wheelchair accessible entrance" == label:
#  elif "Wheelchair accessible parking" == label:
#  elif "Wheelchair accessible restroom" == label:
#  elif "Wheelchair accessible elevator" == label:
#  elif "Non-English interpreter services" == label:
#  elif "ASL interpreter services" == label:
#  elif "Drive-thru options" == label:
#  elif "Non-rapid PCR/NAAT test" == label:
#  elif "Non-rapid PCR/NAAT cost" == label:
#  elif "Non-rapid PCR/NAAT time to get results (hours)" == label:
#  elif "Non-rapid PCR/NAAT test method" == label:
#  elif "Antigen test" == label:
#  elif "Antigen test cost" == label:
#  elif "Antigen test time to get results (hours)" == label:
#  elif "Antibody test" == label:
#  elif "Antibody test cost" == label:
#  elif "Antibody test time to get results (hours)" == label:
#  elif "Rapid PCR/NAAT test" == label:
#  elif "Rapid PCR/NAAT test cost" == label:
#  elif "Rapid PCR/NAAT test time to get results (hours)" == label:
#  elif "Rapid PCR/NAAT test method" == label:
#  elif "At-home tests" == label:
#  elif "At-home test cost" == label:
#  elif "Mail-in test" == label:
#  elif "Mail-in test cost" == label:
#  elif "Mail-in test time to get results (hours)" == label:
#  elif "Also a COVID-19 vaccination a location" == label:
#  elif "COVID-19 vaccination webiste" == label:
#  elif "Other Notes" == label:
  else:
    blob[label] = str(attribute)

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
  parsed = json.loads(result.strip())
  print("<script type=\"application/ld+json\">\n{}\n</script>".format(json.dumps(parsed,indent=4)))

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
