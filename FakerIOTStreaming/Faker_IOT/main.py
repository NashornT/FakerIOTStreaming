import argparse
from faker_iot import FakerIot
from multiprocessing import Process

def start_faker(batchs, time, generate_csv):
    run_faker = FakerIot(batchs, time, generate_csv)
    run_faker.start_streaming()

def main():
    parser = argparse.ArgumentParser(description="Script para geração de dados IOT fakes")
    parser.add_argument("--batchs", type=int, default=1, help="Quantas iterações fará com a API.")
    parser.add_argument("--time", type=int, default=300, help="Intervalo de tempo entre as iterações em segundos.")
    parser.add_argument("--generate_csv", type=bool, default=False, help="Se irá gerar CSVs dos dados fakes.")
    parser.add_argument("--n_devices", type=int, default=1, help="Quantidade de dispositivos simulados.")

    args = parser.parse_args()

    processes = []
    for device_id in range(args.n_devices):
        p = Process(target=start_faker, args=(args.batchs, args.time, args.generate_csv))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == '__main__':
    main()
