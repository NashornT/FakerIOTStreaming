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
    """
    Classe para simular e publicar dados IoT falsos no Google Pub/Sub.

    Args:
        batchs (int): Número de lotes de dados a serem enviados.
        time (int): Intervalo de tempo, em segundos, entre o envio de cada lote.
        generate_csv (bool): Define se os dados devem ser salvos em arquivos CSV.

    Atributos:
        project_id (str): ID do projeto do Google Cloud.
        topic_id (str): ID do tópico Pub/Sub para publicar os dados.
        publisher (pubsub_v1.PublisherClient): Cliente para publicar dados no Pub/Sub.
        topic_path (str): Caminho completo do tópico no Pub/Sub.
    """

    def __init__(self, batchs, time, generate_csv):
        """
        Inicializa a instância da classe FakerIot com as configurações de simulação e publicação.

        Args:
            batchs (int): Número de lotes a serem enviados.
            time (int): Intervalo de tempo em segundos entre os lotes.
            generate_csv (bool): Se True, salva os dados em arquivos CSV.
        """
        self.batchs = batchs
        self.time = time
        self.generate_csv = generate_csv
        self.project_id = project_id  # ID do projeto GCP.
        self.topic_id = topic_id  # ID do tópico Pub/Sub.
        self.publisher = pubsub_v1.PublisherClient()  # Cliente para publicar dados no Pub/Sub.
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)  # Caminho completo do tópico.

    def start_streaming(self):
        """
        Gera e publica dados IoT falsos em lotes para o Google Pub/Sub.

        Para cada lote, gera dados com campos de status, temperatura, umidade e horário, e, se especificado,
        salva os dados em um arquivo CSV. Em seguida, publica todos os dados do lote em formato JSON no tópico
        do Pub/Sub.

        O metodo espera pelo intervalo de tempo especificado entre os envios de lotes e decrementa o contador de lotes
        até que atinja zero.
        """
        while self.batchs > 0:  # Loop para enviar dados em lotes, decrementando o contador de lotes.
            # Define o diretório para salvar o arquivo CSV.
            output_dir = 'output_directory'
            os.makedirs(output_dir, exist_ok=True)

            # Define opções de status com maior probabilidade de ser "Active".
            status_options = ['Active'] * 99 + ['Inactive']

            # Inicializa o gerador de dados falsos e cria estrutura para os dados.
            fake = Faker()
            data = {col['Name']: [] for col in columns}  # Estrutura para armazenar dados falsos.

            # Formata o horário para simular o sensor em formato de string.
            date_fmt = "%H:%M:%S"
            for id in range(20):  # Define o número de dispositivos simulados por lote.
                for col in columns:  # Preenche cada coluna com dados específicos de acordo com o tipo.
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

            # Converte os dados para um DataFrame do pandas.
            df = pd.DataFrame(data)

            # Se habilitado, salva os dados como CSV.
            if self.generate_csv is True:
                file_name = uuid4().hex  # Nome único para o arquivo CSV.
                output_path = os.path.join(output_dir, f'{file_name}.csv')
                df.to_csv(output_path, index=False)  # Salva o DataFrame no CSV.
                print(f"Dados gerados e salvos como {output_path}")

            # Converte cada linha do DataFrame para um formato JSON de mensagem.
            messages = []
            for index, row in df.iterrows():
                message_data = {
                    "device_id": row["device_id"],
                    "timestamp": row["timestamp"],
                    "date": row["date"],
                    "status": row["status"],
                    "data": {
                        "temperature": row["temperature"],
                        "humidity": row["humidity"]
                    }
                }
                messages.append(message_data)

            # Estrutura o lote com `batch_id` e `timestamp` para envio ao Pub/Sub.
            iot_data = {
                "batch_id": f"batch_{str(datetime.now())}",
                "timestamp": str(datetime.now()),
                "device_data": messages
            }

            # Publica o lote como uma única mensagem JSON.
            batch_message = json.dumps(iot_data).encode("utf-8")
            future = self.publisher.publish(self.topic_path, data=batch_message)
            print(f"Publicado lote: {future.result()} - {len(messages)} mensagens")

            # Espera pelo tempo especificado antes de enviar o próximo lote, caso não seja o último.
            if self.batchs != 1:
                sleep(self.time)
            self.batchs -= 1  # Decrementa o contador de lotes.
