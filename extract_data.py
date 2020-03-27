import sys
import csv

first_row = True
collected_data = {}

def collect_data(row, name):
  if name not in collected_data:
    previous_data = [0] * len(row)
  else:
    previous_data = collected_data[name]
  data = []
  for i in xrange(len(row)):
    try:
      datum = int(row[i])
    except:
      datum = 0
    data.append(previous_data[i] + datum)
  collected_data[name] = data

with open(sys.argv[1]) as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    if first_row:
      column_names = row
      column_name_to_index = {}
      for i in xrange(len(column_names)):
        column_name = column_names[i]
        if i == 0 and column_name.startswith('\xef\xbb\xbf'):
          column_name = column_name[3:]
        if column_name == 'Country/Region':
          column_name = 'Country_Region'
        elif column_name == 'Province/State':
          column_name = 'Province_State'
        column_name_to_index[column_name] = i
      first_row = False
    else:
      country = row[column_name_to_index['Country_Region']]
      province = row[column_name_to_index['Province_State']]
      if country == 'US' and ',' in province:
        province = province.split(',')[1].strip()
      collect_data(row, country)
      if province != '':
        combined = country + '/' + province
        collect_data(row, combined)

keys = sorted(collected_data.keys())
cols_to_print = ['Confirmed', 'Deaths', 'Recovered', 'Active']
for key in keys:
  row = [key]
  for col in cols_to_print:
    if col in column_name_to_index:
      row.append(str(collected_data[key][column_name_to_index[col]]))
    else:
      row.append('???')
  print(','.join(row))
