# Software for dinamic extraction of character relashionships from books #

Video preview: https://youtu.be/nnAGQEhnRHs

![screenshot](print_spln.jpg)

NLP applied to the first Harry Potter book ("Harry Potter and the Philosopher's Stone"). Set of tools for dinamic generation of character relashionships from the first Harry Potter book corpus (for every proper noun in the same phrase this tool counts it as a relationship), graph visualization of the relationships, and a tool for name manipulation (changing the 3 main protagonists names in all instances in the full book), etc.
This set of tools were made specifically for the first Harry Potter book (full book in raw txt format in the source-code), but should work with any other book with a few adjustements in the code. This is mainly a NLP tool, created for teaching classes/study, for extracting Proper Nouns and representing them visually, extracting and representing in a graph characters relationship from books, and visually manipulating/dinamic changing characters names.

### Como correr/instalar ###

Para acorrer a aplicação basta iniciar (duplo clique ou via terminal) o ficheiro "main.py" na raiz da aplicação.

É necessária uma versão Python 3.6 ou superior e as seguintes bibliotecas instaladas (exemplo via pip install):

* pip3 install flask
* pip3 install pywebview
* pip3 install networkx
* pip3 install numpy
* pip3 install matplotlib
* pip3 install nltk

Depois de inicializar a aplicação, duas janelas com interface gráfica serão lançadas: a principal, onde se encontram o nome das personagens e opções (Flask+Webview), e uma segunda de apoio onde serão exibidos os grafos seleccionados (Networkx+Matplotlib), por defeito abre um grafo com todas as relações (a janela deverá ser maximizada para melhor visualização). Na janela principal, selecionando "Show Full Graph" será possível visualizar o grafo com todas as realções entre as personagens; selecionando uma personagem em particular será exibido o grafo com as realções apenas associadas a ela.
Nota: na consola são exibidos dados de apoio, como por exemplo os dicionários com os dados para cada realção seleccionada.

### Arquitetura ###
Optamos por criar uma interface gráfica para a aplicação, para facilitar a navegação na informação. Para tal utilizamos uma GUI baseada em Webviews com Flask, ou seja: quando a aplicação principal é lançada (através do ficheiro main.py) é inicializada uma instância da biblioteca “pywebview”, que cria uma janela gráfica com um emulador web (tecnologia semelhante ao “Electrom” no qual foi construído o IDE Atom, por exemplo, moldura gráfica com NodeJS em pano de fundo), que correrá chamadas num servidor local baseado em Flask, sendo este inicializado numa thread paralela, servindo conteúdos na interface gráfica da webview. 

Dividimos a aplicação em módulos lógicos: o package "views" alberga todas as classes relacionadas com a componente gráfica e controladores do Flask; o package "nlp" (abreviatura de Natural Language Processing) alberga todas as classes que trabalham diretamente com o processamento do texto. A classe em "characters.py" é o corçaão da aplicação, efetua a extração dos Nomes Próprios e recorre às restantes classes para apoio: a classe em "graph.py" gera e exibe os grafos; a classe em "nltkFilter.py" recorre à biblioteca NLTK para apoiar na filtragem dos resultados, gerando bigrams, que são depois utilizados para melhor filtrar se um Nome Próprio é nome de personagem ou não (p.e. Hogwarts não é nome de personagem e deve ser excluído). Para exibir os grafos recorremos às bibliotecas NetworkX e Matplotlib. O package "data" contém os dados persistentes, nomeadamente o texto do livro que é carregado automaticmaente no arranque.


### Licença ###
Licença BSD: a aplicação pode ser utilizda ou modificada sem nenhuma restrição.


### Contactos ###
* paulo.jorge.pm@gmail.com
* My Homepage: [www.paulojorgepm.net](www.paulojorgepm.net)
