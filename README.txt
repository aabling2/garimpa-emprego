# GARIMPA EMPREGO

Script de busca aprofundada de empregos em sites que não surgem como primeiras opções nas buscas do google. Utilizando web scraping das páginas 
recolhidas com uso de palavras-chave de ligação com o currículo, habilidades e preferências do indivíduo para definir as prioridades de busca.

*Este programa foi desenvolvido apenas para praticar os conhecimentos em python e outras ferramentas de desenvolvimento web, sem fins de se 
tornar algo comercial porém pensando no funcionamento intuitivo para qualquer usuário.

## Estrutura do projeto

Garimpa_emprego/
*	'-|links/
*	'-|outputs/
	'-|scripts/
		'-|__init__.py
		'-|cv_reader.py
		'-|dictionary.py
		'-|g_emprego.py
		'-|others.py
	'-|static/
		'-|styles.css
	'-|templates/
		'-|index.html
		'-|links.html
	'-|main.py
*	'-|dict.npz
*	'-|presets.npz
*	'-|urls.npz
	'-|README.txt

* Arquivos/pastas gerados por software.


## Pré-requisitos

Seguem abaixo os requisitos para rodar a aplicação e junto os comandos sugeridos para instalação, caso esteja usando Ubuntu.

* Python 3: 		sudo apt-get install python3
* Pip3:				sudo apt-get install python3-pip 
* Flask:			pip3 install Flask
* Numpy:			pip3 install numpy
* Google:			pip install google
* Requests:			pip install requests
* Werkzeug:			pip install Werkzeug
* PyPDF2:			pip install PyPDF2

## Argumentos de entrada

*-h				--Ajuda
*-p 5000			--Porta do servidor local

## Instruções de uso

A aplicação pode ser aberta no navegador a partir do servidor local e porta ativa (ex.:http://localhost:5000).
É possível então carregar um arquivo no formato "pdf" do currículo pessoal e com este efetuar o escaneamento, onde serão coletadas palavras relevantes para utilizar
como palavra-chave, dependendo do grau de refinamento do banco de palavras podem surgir mais ou menos palavras para adicionar, mesmo assim será possível adicionar
novas palavras digitando e clicando no botão de "Add", definindo anteriormente para onde esta palavra deverá ir conforme a seleção por cores para cada nível de busca
ou então a seleção de exclusão que incluirá a palavra no banco de palavras a remover.
Com as palavras-chave definidas pode se então clicar no botão "Pesquisar" para iniciar a coleta de endereços para as pesquisas efetuadas através destas palavras, após
isso será possível extrair o número de palavras-chave existentes em cada página recolhida através do botão "Scrap", o processo poderá demorar nestes dois casos.
Para aplicar os pesos obtidos nos resultados e listar na ordem de relevância basta clicar no botão "Listar resultados", que irá direcionar para a visualização desta 
lista organizada, podendo então abrir e visualizar cada página e salvar ou excluir dos favoritos.
Na página principal ainda é possível modificar o valor do número de buscas a efetuar para cada pesquisa de cada palavra-chave e também os valores dos pesos a serem aplicados.
É possível também efetuar uma cópia dos dados recolhidos em outro dia transformando para a data corrente ou excluir os mesmos, conforme data selecionada. Tantos estes
parâmtros realatados quantos as palavras-chave podem ser salvos com o botão "Salvar Parâmetros".
Caso queira efetuar a pesquisa para todas as palavras de busca registradas e não apenas para o nível primário basta ativar o botão em "Pesquisar tudo".

*Deixei a aplicação rodando sem threads então enquanto o processo estiver executando a página ficara em loading e a atualização das mensagens do processo
aparecerá apenas no console.

Para iniciar o container no Docker:

"sudo docker login"                                                      - Logar no Docker
"sudo docker run -it -p 5000:5000 abling2/python_garimpa_emprego"        - Inicia container da aplicação mapeando a porta 5000 à porta 5000 do host
"sudo docker stop $(docker ps -a -q)"                                    - Para todos containers rodando

## Autor

* **Augusto Abling** - *2020*