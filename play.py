#!/usr/bin/env python

import pandas as pd
from sklearn import neighbors
import gc

# Load Data
d = pd.read_pickle('data')

# Coalesce data
d.lot_size = d.lot_size.combine_first(d.size_m2)
d.latitude = d.latitude.combine_first(d.latitude_vacant)
d.longitude = d.longitude.combine_first(d.longitude_vacant)

# Populate vacancy status for non-vacant parcels
d.loc[d.is_vacant.isna(), 'is_vacant'] = 0

# Remove unnecessary columns
df = d[['assessed_value', 'latitude', 'longitude', 'lot_size', 'is_vacant']]

# Make numeric
df = df.apply(pd.to_numeric)

# Remove parcels without location or lot size
df = df[df.lot_size.notna()]
df = df[df.latitude.notna()]
df = df[df.longitude.notna()]

# Add unit price
df['unit_price'] = df.assessed_value / df.lot_size

# Prep training data. Take vacant lots with assessment values
train = df[df.is_vacant == 1]
train = train[train.unit_price > 0]

trainX = train[['latitude', 'longitude']].to_numpy()
trainY = train[['unit_price']].to_numpy()

# See https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.RadiusNeighborsRegressor.html#sklearn.neighbors.RadiusNeighborsRegressor
model = neighbors.KNeighborsRegressor(
  n_neighbors=train.shape[0], # Use every example
  weights='distance',
  algorithm='kd_tree',
  leaf_size=30,
  p=2,
  metric='minkowski',
  metric_params=None,
  n_jobs=None
)

model_fit = model.fit(trainX, trainY)

# Apply model to full set
predictions = model_fit.predict(df[['latitude', 'longitude']].to_numpy())

# Attach predictions to original set
df['predicted_unit_price'] = pd.Series(predictions)