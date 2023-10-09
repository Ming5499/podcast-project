import psycopg2
import faker

# Create a Faker instance
fake = faker.Faker()


def db_connect():
    conn = psycopg2.connect(
        dbname='podcast',
        user='postgres',
        password='123456',
        host='localhost'
    )

    return conn


def create_table():
    #Create table
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS public.customer
            (
                customer_id integer NOT NULL,
                customer_name character varying(100),
                age integer,
                address character varying(100),
                phone character varying(100),
                email character varying(100),
                CONSTRAINT customer_pkey PRIMARY KEY (customer_id)
            )
        """
    )
    conn.commit()
    cur.close()
    conn.close()
    
    
def populate_table():
    conn = db_connect()
    cur = conn.cursor()
    
    customers = [] 
    for i in range(10):
        customer_data = (
            i,
            fake.name(),
            fake.random_int(min=12, max=65, step=1),
            fake.address(),
            fake.phone_number(),
            fake.email()
        )
        customers.append(customer_data)

            
    cur.executemany(
        """
        INSERT INTO public.customer
        (customer_id, customer_name, age, address, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        customers
    )    
    
    cur.close()
    conn.commit()
    conn.close()
    
    
create_table()
populate_table()