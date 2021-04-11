#!/usr/bin/env python

from sodapy import Socrata
import pandas as pd

# Get Data

yegd = {
  'assessments': 'q7d6-ambg',
  'info': 'dkk9-cj3x',
  'vacant': 'svsw-2ub7'
}

client = Socrata("data.edmonton.ca", None)

limit = 5000000

assessments = pd.DataFrame(client.get(yegd['assessments'], limit=limit))
info = pd.DataFrame(client.get(yegd['info'], limit=limit))
vacant = pd.DataFrame(client.get(yegd['vacant'], limit=limit))

# Join
d = pd.concat([assessments, info])

d['address'] = d.house_number + ' ' + d.street_name
vacant['is_vacant'] = 1

d = d.join(vacant.set_index('address'), on='address', rsuffix='_vacant')

df.to_pickle('data')
