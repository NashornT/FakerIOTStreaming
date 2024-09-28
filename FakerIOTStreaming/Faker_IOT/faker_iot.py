from uuid import uuid4
from time import sleep
import pandas as pd
from faker import Faker
from estrutura import columns
from datetime import datetime
import random
import json
from google.cloud import pubsub_v1
from cloud_setup import *


class FakerIot:

    def __init__(self, batchs, time,generate_csv):
        self.batchs = batchs
        self.time = time
        self.generate_csv = generate_csv
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    def start_streaming(self):


        while self.batchs > 0:
            # Definir o caminho do diretório onde o arquivo será salvo
            output_dir = 'output_directory'
            os.makedirs(output_dir, exist_ok=True)

            # Definir possíveis valores para o campo Status
            status_options = ['Active'] * 99 + ['Inactive']

            # Gerar dados falsos
            fake = Faker()
            data = {col['Name']: [] for col in columns}

            date_fmt = "%H:%M:%S"
            for id in range(20):  # Definindo o número de linhas de dados falsos
                for col in columns:
                    if col['Type'] == 'SENSOR':
                        data[col["Name"]].append(f"sensor{id}")
                    elif col['Type'] == 'TIME':
                        data[col["Name"]].append(str(datetime.now().strftime(date_fmt)))
                    elif col['Type'] == 'TEMPERATURE' or col['Type'] == 'HUMIDITY':
                        data[col["Name"]].append(fake.random_int(min=18, max=80))
                    elif col['Type'] == 'STATUS':
                        data[col["Name"]].append(random.choice(status_options))
                    elif col['Type'] == 'DATE':
                        data[col["Name"]].append(str(datetime.now().date()))


            # Criar o DataFrame
            df = pd.DataFrame(data)

            # Gerar um nome único para o arquivo CSV
            if self.generate_csv is True:
                file_name = uuid4().hex
                output_path = os.path.join(output_dir, f'{file_name}.csv')
                df.to_csv(output_path, index=False)
                print(f"Dados gerados e salvos como {output_path}")

            #df.to_json(output_path)


            messages = []
            for index, row in df.iterrows():
                message_data = {
                    "device_id": row["device_id"],
                    "timestamp": row["timestamp"],
                    "date": row["date"],
                    "status": row["status"],
                    "data":{
                        "temperature": row["temperature"],
                        "humidity": row["humidity"]
                    }
                }
                messages.append(message_data)

            iot_data = {
                "batch_id":f"batch_{str(datetime.now())}",
                "timestamp":str(datetime.now()),
                "device_data":messages
            }

            # Publica o lote inteiro de uma vez
            batch_message = json.dumps(iot_data).encode("utf-8")
            future = self.publisher.publish(self.topic_path, data=batch_message)
            print(f"Publicado lote: {future.result()} - {len(messages)} mensagens")

            # Espera 30 segundos antes de gerar o próximo lote
            if self.batchs != 1:
                sleep(self.time)
            self.batchs -= 1
