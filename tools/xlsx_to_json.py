#!/usr/bin/env python3
from datetime import date
import json
import pandas
import sys

def additional_property(blob, property_name, attribute):
  if "additionalProperty" not in blob:
    blob["additionalProperty"] = []
  property = {}
  property["@type"] = "PropertyValue"
  property["name"] = property_name
  property["value"] = str(attribute)
  blob["additionalProperty"].append(property)

def process_weekday(blob, label, attribute, weekday):
  if "X" == attribute:
    return
  if "openingHours" not in blob:
    blob["openingHours"] = []
  blob["openingHours"].append("{} {}".format(weekday, str(attribute)))

def process_test_type(blob, label, attribute):
  if "No" == attribute:
    return
  if "availableService" not in blob:
    blob["availableService"] = []
  test_info = {}
  test_info["@type"] = "MedicalTest"
  test_info["name"] = str(label)
  blob["availableService"].append(test_info)

def process_test_info(blob, test_type, info_type, attribute):
  tests = blob["availableService"]
  for test in tests:
    if test["name"] != test_type:
      continue
    additional_property(test, info_type, attribute)

def process_attribute(blob, label, attribute):
  if "Name" == label: 
    blob["name"] = attribute
#  elif "Unique ID" == label:
  elif "Address Line 1" == label:
    blob["address"] = str(attribute)
  elif "Address Line 2" == label:
    blob["address"] += ", {}".format(str(attribute)) 
  elif "City or Locality" == label:
    blob["address"] += ", {}".format(str(attribute)) 
  elif "State or Province" == label:
    blob["address"] += ", {}".format(str(attribute)) 
  elif "Postal Code" == label:
    blob["address"] += ", {}".format(str(attribute)) 
  elif "COVID-19 testing website" == label:
    blob["url"] = str(attribute)
  elif "Free COVID-19 tests" == label:
    if "Free for all" == attribute:
      blob["isAccessibleForFree"] = "true"
      blob["priceRange"] = str(attribute)
    elif "Free with insurance" == attribute:
      blob["priceRange"] = str(attribute)
  elif "Phone" == label:
    blob["telephone"] = str(attribute)
  elif "Email" == label:
    blob["email"] = str(attribute)
#  elif "Website" == label:
#  elif "Category" == label:
  elif "Latitude" == label:
    blob["latitude"] = str(attribute)
  elif "Longitude" == label:
    blob["longitude"] = str(attribute)
  elif "Monday" == label:
    process_weekday(blob, label, attribute, "Mo")
  elif "Tuesday" == label:
    process_weekday(blob, label, attribute, "Tu")
  elif "Wednesday" == label:
    process_weekday(blob, label, attribute, "We")
  elif "Thursday" == label:
    process_weekday(blob, label, attribute, "Th")
  elif "Friday" == label:
    process_weekday(blob, label, attribute, "Fr")
  elif "Saturday" == label:
    process_weekday(blob, label, attribute, "Sa")
  elif "Sunday" == label:
    process_weekday(blob, label, attribute, "Su")
#  elif "Appointment required" == label:
#  elif "Referral required" == label:
#  elif "Patient restrictions" == label:
#  elif "Location instructions" == label:
  elif "Insurance accepted" == label:
    blob["healthPlanNetworkId"] = attribute
#  elif "Insurance required" == label:
#  elif "Minimum age" == label:
#  elif "Languages spoken at location" == label:
### TODO: use "knowsLanguage" with IETF BCP 47 Standard
#  elif "Wheelchair accessible entrance" == label:
#  elif "Wheelchair accessible parking" == label:
#  elif "Wheelchair accessible restroom" == label:
#  elif "Wheelchair accessible elevator" == label:
  elif "Non-English interpreter services" == label:
    additional_property(blob, "interpreterServices", attribute)
  elif "ASL interpreter services" == label:
    additional_property(blob, "interpreterServicesASL", attribute)
  elif "Drive-thru options" == label:
    if "Optional" == attribute or "Only" == attribute:
      blob["hasDriveThroughService"] = "true" 
      additional_property(blob, "driveThruOptions", attribute)
  elif "Non-rapid PCR/NAAT test" == label:
    process_test_type(blob, label, attribute)
  elif "     Non-rapid PCR/NAAT cost" == label:
    process_test_info(blob, "Non-rapid PCR/NAAT test", "cost", attribute)
  elif "     Non-rapid PCR/NAAT time to get results (hours)" == label:
    process_test_info(blob, "Non-rapid PCR/NAAT test", "timeToResults", attribute)
  elif "     Non-rapid PCR/NAAT test method" == label:
    process_test_info(blob, "Non-rapid PCR/NAAT test", "testMethod", attribute)
  elif "Antigen test" == label:
    process_test_type(blob, label, attribute)
  elif "     Antigen test cost" == label:
    process_test_info(blob, "Antigen test", "cost", attribute)
  elif "     Antigen test time to get results (hours)" == label:
    process_test_info(blob, "Antigen test", "timeToResults", attribute)
  elif "Antibody test" == label:
    process_test_type(blob, label, attribute)
  elif "     Antibody test cost" == label:
    process_test_info(blob, "Antibody test", "cost", attribute)
  elif "     Antibody test time to get results (hours)" == label:
    process_test_info(blob, "Antibody test", "timeToResults", attribute)
  elif "Rapid PCR/NAAT test" == label:
    process_test_type(blob, label, attribute)
  elif "     Rapid PCR/NAAT test cost" == label:
    process_test_info(blob, "Rapid PCR/NAAT test", "cost", attribute)
  elif "     Rapid PCR/NAAT test time to get results (hours)" == label:
    process_test_info(blob, "Rapid PCR/NAAT test", "timeToResults", attribute)
  elif "     Rapid PCR/NAAT test method" == label:
    process_test_info(blob, "Rapid PCR/NAAT test", "testMethod", attribute)
  elif "At-home tests" == label:
    process_test_type(blob, label, attribute)
  elif "     At-home test cost" == label:
    process_test_info(blob, "At-home tests", "cost", attribute)
  elif "Mail-in test" == label:
    process_test_type(blob, label, attribute)
  elif "     Mail-in test cost" == label:
    process_test_info(blob, "Mail-in test", "cost", attribute)
  elif "     Mail-in test time to get results (hours)" == label:
    process_test_info(blob, "Mail-in test", "timeToResults", attribute)
  elif "Also a COVID-19 vaccination a location" == label:
    additional_property(blob, "vaccineLocation", attribute)
  elif "COVID-19 vaccination webiste" == label:
    additional_property(blob, "vaccinationWebsite", attribute)
  elif "Other Notes" == label:
    additional_property(blob, "notes", attribute)
  else:
    TitleCase_label = ''.join(label.title().split())
    camelCase_label = TitleCase_label[0].lower() + TitleCase_label[1:]
    additional_property(blob, camelCase_label, attribute)

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
