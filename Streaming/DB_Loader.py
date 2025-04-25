"""
Loading the Crash Location and number of units involved in the crash
into our operational DB (Traffic_Crashes) Which is part of our new Crash system.

The rest of the record data will be inserted using our Data entry Desktop app.
"""
from kafka import KafkaConsumer
import pyodbc
import json
import logging
import uuid

# Configuration
DB_CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-N4J2UNJ;"
    "DATABASE=Traffic_Crashes;"
    "Trusted_Connection=yes;"
)
KAFKA_TOPIC = "lat-long-topic"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger()

def create_consumer():
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=['localhost:9092'],
        group_id='DB-loader-group',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def get_next_id(conn):
    """Generate a new UUID-based string ID"""
    return str(uuid.uuid4())

def clean_data(data):
    """Clean and validate incoming data"""
    return {
        'LATITUDE': float(data['LATITUDE']),
        'LONGITUDE': float(data['LONGITUDE']),
        'NUM_UNITS': int(data['NUM_UNITS'])  # Add this line
    }


def load_to_DB(conn, data, crash_id):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Crashes (
            CRASH_RECORD_ID, 
            LATITUDE,
            LONGITUDE,
            NUM_UNITS									
        ) VALUES (?, ?, ?, ?)
        """, 
        crash_id,
        data['LATITUDE'],
        data['LONGITUDE'],
        data['NUM_UNITS'],
        )
        conn.commit()
        logger.info(f"Inserted record with ID: {crash_id}")
        return True
    except Exception as e:
        logger.error(f"DB Error: {str(e)}")
        return False

def run_loader():
    consumer = create_consumer()
    conn = pyodbc.connect(DB_CONN_STR)
    logger.info("DB Loader started (Ctrl+C to stop)")
    
    try:
        for message in consumer:
            try:
                data = clean_data(message.value)
                crash_id = get_next_id(conn)
                if load_to_DB(conn, data, crash_id):
                    consumer.commit()
            except (KeyError, ValueError) as e:
                logger.error(f"Invalid data: {str(e)}")
            except json.JSONDecodeError:
                logger.error("Invalid message format")
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        conn.close()
        consumer.close()

if __name__ == "__main__":
    run_loader()
