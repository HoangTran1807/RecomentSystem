import pandas as pd

# Read product data
products = pd.read_json('product_data1.json')

# List of product IDs
resultID = [3320, 1084, 6183, 3150, 4862, 7174, 3701, 3514, 1789, 3086]

# Get products with IDs in resultID
selected_products = products[products['Id'].isin(resultID)]

# Write selected products to JSON file
selected_products.to_json('result.json', orient='records')