import os
import json
import requests
import xmltodict

from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook


from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

PODCAST_URL = "https://www.marketplace.org/feed/podcast/marketplace/"
EPISODE_FOLDER = "episodes"
FRAME_RATE = 16000



def create_database():
    create_database = PostgresOperator(
        task_id='create_table_postgres',
        sql="""
        CREATE TABLE IF NOT EXISTS episodes (
            link TEXT PRIMARY KEY,
            title TEXT,
            filename TEXT,
            published TEXT,
            description TEXT,
            transcript TEXT
        );
        """,
        postgres_conn_id="podcasts"  #PostgreSQL connection ID that connected
    )
    return create_database



def get_episodes():
    data = requests.get(PODCAST_URL)
    feed = xmltodict.parse(data.text)
    episodes = feed["rss"]["channel"]["item"]
    print(f"Found {len(episodes)} episodes.")
    return episodes



def load_episodes(episodes):
    hook = PostgresHook(postgres_conn_id="podcasts")
    
    stored_episodes = hook.get_pandas_df("SELECT * from episodes;")
    new_episodes = []
    for episode in episodes:
        #Check if episode already in database
        if episode["link"] not in stored_episodes["link"].values: #link (primary key) is unique
            filename = f"{episode['link'].split('/')[-1]}.mp3" #take the last part in link and create mp3 name
            new_episodes.append([episode["link"], episode["title"], episode["pubDate"], episode["description"], filename])

    hook.insert_rows(table='episodes', rows=new_episodes, target_fields=["link", "title", "published", "description", "filename"])
    return new_episodes



def download_episodes(episodes):
    audio_files = []
    for episode in episodes:
        name_end = episode["link"].split('/')[-1]
        filename = f"{name_end}.mp3"
        audio_path = os.path.join(EPISODE_FOLDER, filename)
        if not os.path.exists(audio_path):
            print(f"Downloading {filename}")
            audio = requests.get(episode["enclosure"]["@url"])
            with open(audio_path, "wb+") as f:
                f.write(audio.content)
        audio_files.append({
            "link": episode["link"],
            "filename": filename
        })
    return audio_files



def speech_to_text(audio_files, new_episodes):
    hook = SqliteHook(sqlite_conn_id="podcasts")
    untranscribed_episodes = hook.get_pandas_df("SELECT * from episodes WHERE transcript IS NULL;")

    model = Model(model_name="vosk-model-en-us-0.22-lgraph")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)

    for index, row in untranscribed_episodes.iterrows():
        print(f"Transcribing {row['filename']}")
        filepath = os.path.join(EPISODE_FOLDER, row["filename"])
        mp3 = AudioSegment.from_mp3(filepath)
        mp3 = mp3.set_channels(1)
        mp3 = mp3.set_frame_rate(FRAME_RATE)

        step = 20000
        transcript = ""
        for i in range(0, len(mp3), step):
            print(f"Progress: {i/len(mp3)}")
            segment = mp3[i:i+step]
            rec.AcceptWaveform(segment.raw_data)
            result = rec.Result()
            text = json.loads(result)["text"]
            transcript += text
        hook.insert_rows(table='episodes', rows=[[row["link"], transcript]], target_fields=["link", "transcript"], replace=True)


