import argparse
from faker_iot import FakerIot
from multiprocessing import Process

def start_faker(batchs, time, generate_csv):
    """
    Inicializa e inicia o streaming de dados IoT falsos usando a classe FakerIot.

    Args:
        batchs (int): Número de lotes a serem gerados e enviados.
        time (int): Intervalo de tempo entre o envio de cada lote, em segundos.
        generate_csv (bool): Indica se os dados devem ser salvos em arquivos CSV.
    """
    run_faker = FakerIot(batchs, time, generate_csv)
    run_faker.start_streaming()  # Inicia o streaming de dados fakes.


def main():
    """
    Função principal para configurar e iniciar a geração de dados IoT falsos.

    Utiliza `argparse` para receber argumentos de linha de comando que configuram:
        - A quantidade de lotes (`batchs`) a serem enviados.
        - O intervalo de tempo (`time`) entre os envios de cada lote.
        - A opção de gerar CSVs dos dados falsos (`generate_csv`).
        - A quantidade de dispositivos simulados (`n_devices`).

    Para cada dispositivo simulado, cria um processo separado que chama a função `start_faker`
    para gerar e enviar dados falsos em paralelo.
    """

    # Configuração do parser de argumentos para aceitar parâmetros de linha de comando.
    parser = argparse.ArgumentParser(description="Script para geração de dados IOT fakes")
    parser.add_argument("--batchs", type=int, default=1, help="Quantas iterações fará com a API.")
    parser.add_argument("--time", type=int, default=300, help="Intervalo de tempo entre as iterações em segundos.")
    parser.add_argument("--generate_csv", type=bool, default=False, help="Se irá gerar CSVs dos dados fakes.")
    parser.add_argument("--n_devices", type=int, default=1, help="Quantidade de dispositivos simulados.")

    # Armazena os argumentos fornecidos pelo usuário.
    args = parser.parse_args()

    # Cria uma lista para armazenar os processos que serão iniciados.
    processes = []
    # Para cada dispositivo simulado, cria um novo processo.
    for device_id in range(args.n_devices):
        # Define o processo com a função `start_faker` e os argumentos coletados.
        p = Process(target=start_faker, args=(args.batchs, args.time, args.generate_csv))
        processes.append(p)  # Adiciona o processo à lista de processos.
        p.start()  # Inicia o processo de simulação para o dispositivo.

    # Espera até que todos os processos sejam concluídos.
    for p in processes:
        p.join()

# Executa a função principal `main()` ao iniciar o script diretamente.
if __name__ == '__main__':
    main()