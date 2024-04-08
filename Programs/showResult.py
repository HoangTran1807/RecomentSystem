import pandas as pd

# Read product data
products = pd.read_json('product_data.json')

# List of product IDs
resultID = [1280, 1281, 1284, 1306, 1359, 1361, 1363, 1364, 1365, 1369]

# Get products with IDs in resultID
selected_products = products[products['Id'].isin(resultID)]

# Write selected products to JSON file
selected_products.to_json('result.json', orient='records')