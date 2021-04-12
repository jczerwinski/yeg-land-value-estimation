#!/usr/bin/env python

import math

import pandas as pd

from sklearn import neighbors
from sklearn.model_selection import cross_validate

from sklearn.metrics import explained_variance_score
from sklearn.metrics import max_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_poisson_deviance
from sklearn.metrics import mean_gamma_deviance
from sklearn.metrics import mean_absolute_percentage_error

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
model = neighbors.RadiusNeighborsRegressor(
  radius=math.inf, # Use every example
  weights='distance',
  algorithm='kd_tree',
  leaf_size=30,
  p=2,
  metric='minkowski',
  metric_params=None,
  n_jobs=None
)

scoring = [
  'explained_variance',
  'max_error',
  'neg_mean_absolute_error',
  'neg_mean_squared_error',
  'neg_root_mean_squared_error',
  'neg_mean_squared_log_error',
  'neg_median_absolute_error',
  'r2',
  'neg_mean_poisson_deviance',
  'neg_mean_gamma_deviance',
  'neg_mean_absolute_percentage_error'
]

# Cross-validate and score the model
scores = cross_validate(model, trainX, trainY, scoring=scoring)

# Print the results
scores

# Train model on full training set
# model_fit = model.fit(trainX, trainY)

# # Apply model to full set
# predictions = model_fit.predict(df[['latitude', 'longitude']].to_numpy())

# # Attach predictions to original set
# df['predicted_unit_price'] = pd.Series(predictions[:,0]).tolist()

# # Add error measures
# df['predicted_unit_price_error'] = df.predicted_unit_price - df.unit_price
# df['predicted_unit_price_relative_error'] = df.predicted_unit_price / df.unit_price

# # Save data
# df.to_pickle('data_with_predictions')

# sns.displot(df.predicted_unit_price_error, binwidth=100)
# plt.pyplot.show()

# sns.displot(df.predicted_unit_price, binwidth=10)
# plt.pyplot.show()

# sns.displot(df.unit_price)
# plt.pyplot.show()
