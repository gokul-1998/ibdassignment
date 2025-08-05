from kafka import KafkaProducer
import time

# Configuration
TOPIC = 'test-topic'
BATCH_SIZE = 10
MAX_RECORDS = 1000
SLEEP_TIME = 10  # seconds

# Connect to Kafka (adjust bootstrap_servers as needed)
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Read data from file
with open('data.txt', 'r') as file:
    lines = file.readlines()

# Send data in batches
count = 0
for i in range(0, min(len(lines), MAX_RECORDS), BATCH_SIZE):
    batch = lines[i:i + BATCH_SIZE]
    for record in batch:
        producer.send(TOPIC, record.strip().encode('utf-8'))
        count += 1
        print(f'Sent record {count}: {record.strip()}')
    
    producer.flush()
    
    if count >= MAX_RECORDS:
        break
    
    print(f'Batch of {BATCH_SIZE} sent. Sleeping for {SLEEP_TIME}s...')
    time.sleep(SLEEP_TIME)

print('Finished sending 1000 records.')
