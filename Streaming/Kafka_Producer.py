"""
    This Kafka producer is a simulation for
    Emergency sending crash location
    to Chicago police via API
"""
from kafka import KafkaProducer
import csv
import time
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger()

def clean_column_name(name):
    """Remove BOM and normalize column names"""
    return name.replace('\ufeff', '').strip()

def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        compression_type='gzip'
    )

def validate_and_convert(row):
    """Convert numeric fields while preserving all columns"""
    processed = {}
    for key, value in row.items():
        clean_key = clean_column_name(key)
        try:
            # Convert known numeric fields
            if clean_key in ['LATITUDE', 'LONGITUDE', 'POSTED_SPEED_LIMIT', 'NUM_UNITS', 'UNIT_NO']:
                if value:  # Only convert if not empty
                    processed[clean_key] = float(value) if clean_key in ['LATITUDE', 'LONGITUDE'] else int(float(value))
            else:
                processed[clean_key] = value
        except (ValueError, TypeError):
            processed[clean_key] = value  # Keep original if conversion fails
    return processed

def stream_to_kafka():
    producer = create_kafka_producer()
    
    try:
        with open('lat & long & num_units.csv', mode='r', encoding='utf-8-sig') as infile:
            reader = csv.DictReader(infile)
            # Clean column names
            reader.fieldnames = [clean_column_name(name) for name in reader.fieldnames]
            logger.info(f"Detected columns: {reader.fieldnames}")
            
            for row in reader:
                print(f"\n📤 Raw CSV row: {row}")
                
                # Process all columns while converting known numeric fields
                processed = validate_and_convert(row)
                
                if processed:
                    producer.send('lat-long-topic', value=processed)
                    logger.info(f"Sent to Kafka: {json.dumps(processed, indent=2)}")
                else:
                    logger.warning("Skipping invalid row")
                time.sleep(1)
                
    except FileNotFoundError:
        logger.error("CSV file not found")
    except KeyboardInterrupt:
        logger.info("Stopping producer...")
    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    stream_to_kafka()
