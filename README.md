# Projeto de Geração de Dados IoT Falsos
Este projeto é um script simples para a geração de dados IoT falsos usando a biblioteca FakerIot. 
Ele permite a configuração de iterações, intervalo de tempo entre as iterações e a opção de gerar arquivos CSV com os dados falsos.
Além de possibilitar a execução paralela para representar diversos dispositivos gerando dados


## Como usar
O script pode ser executado diretamente da linha de comando e possui três parâmetros principais:

* ```--batchs```: Define quantas iterações a API realizará para gerar os dados. (padrão: 1)
* ```--time```: Define o intervalo de tempo, em segundos, entre uma iteração e outra. (padrão: 300 segundos)
* ```--generate_csv```: Define se será gerado um arquivo CSV com os dados falsos gerados. (padrão: False)
* ```--n_devices```: Define o número  de dispositos que irão gerar dados.

## Exemplo de execução
Execute o script com os parâmetros desejados:


```bash
python nome_do_script.py --batchs 10 --time 60 --generate_csv True --n_devices 2
```

Neste exemplo, o script será executado com:

* 10 iterações
* Intervalo de 60 segundos entre as iterações
* Geração de arquivos CSV com os dados
* 2 dispositivos irão gerar 10 iterações

## Parâmetros
| Parâmetro	         | Tipo  | Descrição                                     | Padrão |
|--------------------|-------|-----------------------------------------------|--------|
 | ```--batchs```     | 	int  | 	Número de iterações que o script fará.       | 	1     |
| ```--time```	      | int   | 	Intervalo de tempo entre as iterações (seg). | 	300   |
| ```--generate_csv``` | 	bool | 	Se os dados gerados serão salvos em CSV.     | 	False |
| ```--n_devices``` | 	int  | 	 Número de dispositivos                      | 	1     |

## Funcionamento

1. O script usa a classe FakerIot para gerar dados de sensores IoT falsos. Ao rodar o script:
2. O número de iterações será determinado pelo valor do argumento --batchs.
3. O intervalo de tempo entre as iterações será controlado pelo argumento --time.
4. Se o argumento --generate_csv for definido como True, os dados gerados serão salvos em arquivos CSV.
5. O argumento --n_devices irá definir quantos dispositivos irão gerar as iterações.

## Contribuindo
Sinta-se à vontade para fazer melhorias ou reportar problemas abrindo issues ou pull requests.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
