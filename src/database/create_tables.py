
from src.database.database import Base, engine
from src.database import models

try:
    Base.metadata.create_all(bind=engine)
    print("All database tables created successfully!")

    print("Tables created:")
    for table_name in Base.metadata.tables:
        print("-", table_name)

except Exception as error:
    print("Error creating tables:", error)
