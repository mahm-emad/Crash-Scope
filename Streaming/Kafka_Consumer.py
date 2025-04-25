from kafka import KafkaConsumer
import requests
import json
from datetime import datetime, timezone, timedelta
import logging

# ===== POWER BI CONFIGURATION =====
POWER_BI_URL = "https://api.powerbi.com/beta/b97ced59-fd70-450d-98e2-7fde19a6beeb/datasets/838aad3d-42b1-438c-84d7-21f8487bd104/rows?key=LG%2Bk%2BeXPKzNRmfbzM1Hrx0AfJv%2FiGapNhEM5JInFrNwX8ax8Y47cSOMknOlex7NHC0LXzeKMtz1NeA%2BiUIlPuw%3D%3D"

# ===== TIMEZONE SETTINGS =====
TZ_OFFSET = timedelta(hours=2)  # UTC+2 for your timezone

# ===== LOGGING SETUP =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger()

def get_localized_timestamp():
    """Returns current time in UTC+2 as ISO string"""
    return (datetime.now(timezone.utc) + TZ_OFFSET).isoformat()

def clean_kafka_message(message):
    """Removes BOM characters and validates fields"""
    clean_data = {k.replace('\ufeff', ''): v for k, v in message.items()}
    
    # Validate required fields
    required_fields = ['NUM_UNITS', 'LATITUDE', 'LONGITUDE']
    if not all(field in clean_data for field in required_fields):
        raise ValueError(f"Missing required fields. Needs: {required_fields}")
    
    return clean_data

def create_consumer():
    """Configure Kafka consumer connection"""
    return KafkaConsumer(
        'lat-long-topic',  # Must match your producer's topic name
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def send_to_powerbi(data):
    """Sends data to Power BI with UTC+2 timestamps"""
    payload = [{
        "NUM_UNITS": int(data['NUM_UNITS']),
        "LATITUDE": float(data['LATITUDE']),
        "LONGITUDE": float(data['LONGITUDE']),
        "CRASH_DATE": get_localized_timestamp()
    }]
    
    try:
        response = requests.post(
            POWER_BI_URL,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=5
        )
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Power BI API Error: {str(e)}")
        return False

def run_consumer():
    """Main consumer loop"""
    logger.info("Starting Kafka Consumer (UTC+2)")
    
    consumer = create_consumer()
    try:
        for message in consumer:
            try:
                clean_data = clean_kafka_message(message.value)
                
                if send_to_powerbi(clean_data):
                    logger.info(f"✅ Success: {clean_data['NUM_UNITS']} units at {get_localized_timestamp()}")
                else:
                    logger.warning("Failed to update Power BI")
                    
            except ValueError as e:
                logger.error(f"Invalid data: {str(e)}")
            except Exception as e:
                logger.error(f"Processing error: {str(e)}")
                
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
    finally:
        consumer.close()
        logger.info("Consumer stopped")

if __name__ == "__main__":
    run_consumer()