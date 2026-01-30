# Notebooks de Validação de Metodologia

Este repositório tem dois notebooks, [SAUDE.ipynb](SAUDE.ipynb) e [SIM_MONTE_CARLO.ipynb](SIM_MONTE_CARLO.ipynb), que servem de documentação para suas respectivas metodologias. \

Este repositório foi feito com base em:
1) https://github.com/sepep-pmsp/dash_onibus_eletricos.git
2) https://github.com/sepep-pmsp/onibus_eletricos_saude.git

## OS DADOS
O dados necessários para rodar os notebooks deste repositório podem ser encontrados neste link: https....\

1) Realize o download do arquivo data.zip dentro da pasta do repositório clonado.
2) Descompacte a pasta com os dados.
3) Confira se a estrutura das pasta é: `data/manual_data/`. Caso a estrutura não seja essa, os notebooks darão erro ao carregar os arquivos csv.
4) Dentro de `data/manual_data/` precisam ter 2 arquivos: `calculo-emissao-poluentes-diario_2025-12-31_silver.csv` (necessário para rodar o SIM_MONTE_CARLO.ipynb) e `linestring_2025-12-31_silver.csv` (necessário para rodar o SAUDE.ipynb).

Ambos os arquivos são compostos por dados reais e públicos, extraídos da API do Olho Vivo no dia 31 de dezembro de 2025 por nossa equipe. \

Outros dados usados são os de setores censitários do IBGE (censo de 2022), que são baixados e tratados automaticamente pelas função em [setores_censitarios.ipynb](setores_censitarios.py), chamadas no notebook [SAUDE.ipynb](SAUDE.ipynb).

## [SIMULAÇÃO DE MONTE CARLO](SIM_MONTE_CARLO.ipynb)

Este notebook demonstra como estamos realizando a Simulação de Monte Carlo para criar cenários hipotéticos, em que alguns dos ônibus a diesel da cidade fossem ônibus elétricos. Na atual versão, estamos apenas considerando a emissão de CO2, mas a mesma metodologia será usada para os demais poluentes e para a quantidade de pessoas afetadas. \

Nosso obetivo é poder criar cenários em tomando por ponto de partida tanto a quantidade de ônibus a diesel a serem substituídos por elétricos, retornando assim quanto de emissão de CO2 seria evitada por dia e por ano; quanto a quantidade de emissão que deve ser evitada, retornando a quantidade de ônibus a serem substituídos necessária para alcança essa meta.

## [SAUDE](SAUDE.ipynb)

Neste notebook demonstramos como estimamos a quantidade de pessoas afetadas pelos poluentes MP e NOx. Nossa metodologia leva em consideração apenas os moradores da região, por usar os setores censitários.