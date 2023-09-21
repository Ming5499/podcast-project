from faker import Faker
import csv
import time
import random

def generate_fake_customer_data(batch_size, num_batches):
    # Create a Faker instance
    fake = Faker()

    # Define the fields you want in your CSV
    fields = ['name', 'age', 'address', 'sex', 'email', 'job']

    # Generate and save customer data in batches
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
                'job': fake.job()
            }
            fake_data_list.append(fake_data)

        # Define the CSV file name for each batch
        csv_file = f"fake_customer_data_batch_{batch_num + 1}.csv"

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

    print("All batches of customer data generated and saved.")

def generate_fake_order_data(batch_size, num_batches):
    # Create a Faker instance
    fake = Faker()

    # Define the fields you want in your CSV
    fields = ['customer_id', 'order_date', 'total_price']

    # Generate and save order data in batches
    for batch_num in range(num_batches):
        fake_data_list = []
        start_time = time.time()  # Record start time
        for i in range(batch_size):
            fake_data = {
                'customer_id': fake.random_int(min=1, max=batch_size),  # Generate random customer IDs
                'order_date': fake.date_between(start_date='-1y', end_date='today'),  # Random order date within the last year
                'total_price': round(random.uniform(10.0, 500.0), 2)  # Random total price
            }
            fake_data_list.append(fake_data)

        # Define the CSV file name for each batch
        csv_file = f"fake_orders_data_batch_{batch_num + 1}.csv"

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

    print("All batches of order data generated and saved.")


def generate_fake_podcast_data(max_podcast_id, titles_file_path, output_file_path):
    # Read podcast titles from the provided file with UTF-8 encoding
    titles = []
    with open(titles_file_path, 'r', encoding='utf-8', newline='') as title_file:
        reader = csv.reader(title_file)
        for row in reader:
            titles.append(row[0])  # Assuming the titles are in the first column

    # Create a list of unique podcast names from the titles file
    unique_podcast_names = list(set(titles))

    # Generate random podcast data
    podcast_data = []
    for podcast_id in range(1, max_podcast_id + 1):
        podcast_name = random.choice(unique_podcast_names)
        price = round(random.uniform(1.0, 10.0), 2)  # Random price between 1.00 and 10.00
        podcast_data.append((podcast_id, podcast_name, price))

    # Write the fake podcast data to the specified output CSV file
    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['podcast_id', 'podcast_name', 'price'])  # Write header
        writer.writerows(podcast_data)

    print(f"Fake podcast data generated and saved to {output_file_path}")


def generate_fake_orders_detail_data(max_order_id, max_podcast_id, output_file_path):
    # Generate random orders_detail data
    orders_detail_data = []
    for order_id in range(1, max_order_id + 1):
        podcast_id = random.randint(1, max_podcast_id)
        quantity = random.randint(1, 10)  # Random quantity between 1 and 10
        orders_detail_data.append((order_id, podcast_id, quantity))

    # Write the fake orders_detail data to the specified output CSV file
    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['order_id', 'podcast_id', 'quantity'])  # Write header
        writer.writerows(orders_detail_data)

    print(f"Fake orders_detail data generated and saved to {output_file_path}")


generate_fake_customer_data(batch_size=20000, num_batches=5)
generate_fake_order_data(batch_size=20000, num_batches=5)
generate_fake_podcast_data(max_podcast_id=50, titles_file_path='csv/titles.csv', output_file_path='csv/fake_podcast_data.csv')
generate_fake_orders_detail_data(max_order_id=20000, max_podcast_id=50, output_file_path='fake_orders_detail_data.csv')