import pandas as pd
import yaml

# Create a sample DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'London', 'Paris']}
df = pd.DataFrame(data)

# Convert DataFrame to a dictionary
df_dict = df.to_dict(orient='records')

# Save dictionary as YAML file
with open('output.yaml', 'w') as file:
    yaml.safe_dump(df_dict, file)

print("DataFrame converted to YAML successfully.")


