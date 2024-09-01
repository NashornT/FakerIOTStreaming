import os
from uuid import uuid4
from time import sleep
import pandas as pd
from faker import Faker
from estrutura import columns
import random

class FakerIot:

    def __init__(self, time):
        self.time = time

    def start_streaming(self):

        while self.time > 0:
            # Definir o caminho do diretório onde o arquivo será salvo
            output_dir = 'output_directory'
            os.makedirs(output_dir, exist_ok=True)

            # Definir possíveis valores para o campo Status
            status_options = ['Active', 'Inactive','Active','Active','Active','Active']

            # Passo 2: Gerar dados falsos
            fake = Faker()
            data = {col['Name']: [] for col in columns}

            for id in range(10):  # Definindo o número de linhas de dados falsos
                for col in columns:
                    if col['Type'] == 'SENSOR':
                        data[col["Name"]].append(f"sensor{id}")
                    elif col['Type'] == 'TIME':
                        data[col["Name"]].append(fake.time())
                    elif col['Type'] == 'TEMPERATURE' or col['Type'] == 'HUMIDITY':
                        data[col["Name"]].append(fake.random_int(min=18, max=80))
                    elif col['Type'] == 'STATUS':
                        data[col["Name"]].append(random.choice(status_options))

            # Passo 3: Criar o DataFrame
            df = pd.DataFrame(data)

            file_name = uuid4().hex

            # Passo 4: Salvar como um arquivo Parquet no diretório especificado
            output_path = os.path.join(output_dir, f'{file_name}.csv')
            df.to_csv(output_path, index=False)

            print(f"Dados gerados e salvos como {output_path}")

            sleep(30)
            self.time = self.time - 1

