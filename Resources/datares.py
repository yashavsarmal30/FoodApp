from database import Database  # Adjust this import based on your project

# Raw multiline string of restaurant data
raw_data = """
4,13,Balakrishna,hotel,"Irla , Vile Parla west ,Mumbai",3.90,t,753698421,excellence of more then 2 decade
5,14,David's Diner,Fast Food,"123 Oak Street, Springfield",4.80,t,555-1234,A cozy diner offering classic American dishes.
6,15,Elizabeth's Eatery,Hotel,"456 Elm Street, Rivertown",4.50,t,555-5678,A charming restaurant serving delicious Mediterranean dishes.
7,16,Christopher's Cafe,Cafe,"789 Maple Avenue, Lakeside",4.70,t,555-9012,An Italian cafe known for its authentic pasta and pizza.
8,17,Mary's Bistro,Fast Food,"101 Pine Street, Hillcrest",4.60,t,555-3456,A sophisticated bistro offering classic French dishes.
9,18,Daniel's Deli,Cafe,"234 Walnut Street, Woodland",4.40,t,555-7890,A cozy deli serving a variety of delicious sandwiches.
10,19,Patricia's Pizzeria,Fast Food,"345 Cedar Street, Seaview",4.90,t,555-2345,A family-friendly pizzeria with a wide selection of toppings.
11,20,John's Joint,Hotel,"456 Oak Street, Riverdale",4.70,t,555-6789,A popular steakhouse known for its juicy steaks and elegant ambiance.
12,21,Tasty Tacos,Fast Food,"456 Tacos Street, Taco City",4.30,t,555-5678,A delicious taco spot serving authentic Mexican cuisine.
"""

# Function to parse a single line into a tuple
def parse_restaurant_line(line: str):
    import csv
    from io import StringIO

    f = StringIO(line)
    reader = csv.reader(f)
    parts = next(reader)

    owner_user_id = int(parts[1])
    name = parts[2]
    restaurant_type = parts[3]
    location = parts[4]
    rating = float(parts[5])
    is_active = parts[6].lower() == 't'
    contact_number = parts[7] if parts[7] else None
    description = parts[8] if len(parts) > 8 else None

    return (owner_user_id, name, restaurant_type, location, rating, is_active, contact_number, description)

# Parse all lines
lines = raw_data.strip().splitlines()
restaurant_data = [parse_restaurant_line(line) for line in lines]

# SQL Insert Query
insert_query = """
INSERT INTO Restaurants (owner_user_id, name, restaurant_type, location, rating, is_active, contact_number, description)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

# Execute insertions
for entry in restaurant_data:
    Database.execute(insert_query, entry)

print(f"✅ Successfully inserted {len(restaurant_data)} records into the Restaurants table.")
