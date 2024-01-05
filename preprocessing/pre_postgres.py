import psycopg2
from utils.constants import * 

def db_connect():
    conn = psycopg2.connect(
        dbname= DATABASE_NAME,
        user= DATABASE_USER,
        password= DATABASE_PASSWORD,
        host= DATABASE_HOST
    )

    return conn


def create_fakedata_tables():
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
            
        CREATE TABLE IF NOT EXISTS public.orders
            (
                order_id integer NOT NULL DEFAULT,
                customer_id integer NOT NULL,
                order_date date,
                total_price numeric(10,2),
                CONSTRAINT orders_pkey PRIMARY KEY (order_id),
                CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id)
                    REFERENCES public.customer (customer_id)
            )
            
        CREATE TABLE IF NOT EXISTS public.orders_detail
            (
                order_id integer NOT NULL DEFAULT,
                podcast_id integer NOT NULL,
                quantity integer,
                CONSTRAINT orders_detail_pkey PRIMARY KEY (order_id),
                CONSTRAINT orders_detail_order_id_fkey FOREIGN KEY (order_id)
                    REFERENCES public.orders (order_id)
                CONSTRAINT orders_detail_podcast_id_fkey FOREIGN KEY (podcast_id)
                    REFERENCES public.podcast (podcast_id) 
            )
    
        CREATE TABLE IF NOT EXISTS public.podcast
            (
                podcast_id integer NOT NULL DEFAULT ,
                podcast_name character varying(100) NOT NULL,
                price numeric(10,2),
                CONSTRAINT podcast_pkey PRIMARY KEY (podcast_id)
            )
            
        """
    )
    conn.commit()
    cur.close()
    conn.close()
    
    
