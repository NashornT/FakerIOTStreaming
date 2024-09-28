import argparse
from faker_iot import FakerIot


def main():
    parser = argparse.ArgumentParser(description="Script para geração de dados IOT fakes")
    parser.add_argument("--batchs",type=int, default=1 ,help="Quantas Iteração fará com a API.")
    parser.add_argument("--time",type=int, default=300 ,help="Intervalo de tempo de uma iteração até a outro em segundos.")
    parser.add_argument("--generate_csv",type=bool, default=False ,help="Se irá gerar csvs do dados fakes.")

    args = parser.parse_args()

    run_faker = FakerIot(args.batchs,args.time,args.generate_csv)
    run_faker.start_streaming()

if __name__ == '__main__':
    main()
