import os
from Resources.database import Database

def init_database():
    # Read the schema file
    schema_path = os.path.join(os.path.dirname(__file__), 'Database', 'PostgreSchema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()

    # Split the schema into individual statements
    statements = schema.split(';')

    # Execute each statement
    for statement in statements:
        if statement.strip():
            Database.execute(statement)

    print("✅ Database schema created successfully!")

    # Create a sample admin user
    admin_query = """
    INSERT INTO Users (name, username, email, password, is_admin)
    VALUES ('Admin User', 'admin', 'admin@example.com', 'admin123', TRUE)
    ON CONFLICT (email) DO NOTHING;
    """
    Database.execute(admin_query)
    print("✅ Admin user created successfully!")

if __name__ == '__main__':
    init_database() 