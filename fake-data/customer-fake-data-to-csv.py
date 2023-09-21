from faker import Faker
import csv
import time

# Create a Faker instance
fake = Faker()

# Define the number of records to generate in each batch
batch_size = 200000
num_batches = 5  

# Define the fields you want in your CSV
fields = ['name', 'age', 'address', 'sex', 'email', 'job']

# Generate and save data in batches
for batch_num in range(num_batches):
    fake_data_list = []
    start_time = time.time()  # Record start time
    for i in range(batch_size):
        fake_data = {
            'name': fake.name(),
            'age': fake.random_int(min=12, max=65, step=1),
            'address': fake.address(),
            'sex': fake.random_element(elements=('Male', 'Female')),
            'email': fake.email(),
            '': fake.job()
        }
        fake_data_list.append(fake_data)

    # Define the CSV file name for each batch
    csv_file = f"fake_data_batch_{batch_num + 1}.csv"

    # Write the fake data to the CSV file for each batch
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        
        # Write the header
        writer.writeheader()
        
        # Write the data rows
        for fake_data in fake_data_list:
            writer.writerow(fake_data)

    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Batch {batch_num + 1} saved to {csv_file} (Time: {elapsed_time:.3f} seconds)")

print("All batches generated and saved.") 
