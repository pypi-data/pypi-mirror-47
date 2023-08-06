[![Build Status](https://travis-ci.org/jecamanga/simples.svg?branch=master)](https://travis-ci.org/jecamanga/simples)
[![Build Status](https://dev.azure.com/simplesgit/simples/_apis/build/status/jecamanga.simples?branchName=master)](https://dev.azure.com/simplesgit/simples/_build/latest?definitionId=1&branchName=master)
[![Documentation Status](https://readthedocs.org/projects/simples/badge/?version=latest)](https://simples.readthedocs.io/pt/latest/?badge=latest)
[![codecov](https://codecov.io/gh/jecamanga/simples/branch/master/graph/badge.svg)](https://codecov.io/gh/jecamanga/simples)

simples
=======================

O pacote simples contém a seguinte estrutura

```
    simples/
        ├── setup.py
        |── simples/
        |       |──── __init__.py
        |       └──── soma.py
        |── tests/
        |      |──── __init__.py
        |      └──── test_soma.py
        └── docs/
```

### Criando a pasta docs e construindo o html:

**Pré requisitos**:

* ``sphinx-build`` para construir a documentação

A pasta docs e seu conteúdo pode ser criada usando os seguintes comandos:

```console
foo@bar:~/simples$ mkdir docs
foo@bar:~/simples$ cd docs
foo@bar:~/simples/docs$ sphinx-quickstart
foo@bar:~/simples/docs$ sphinx-apidoc -f -o source/ ../simples
```

Dentro da pasta vários arquivos são criados, sendo alguns deles ``conf.py`` e ``index.rst``. 

#### Modificando o ``conf.py``

* O pacote ``simples`` utiliza o padrão de [docstring do numpy](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard). Então deverá ser inserida essa informação na lista ``extensões`` que se encontra dentro do arquivo. 
```python
extensions = ['sphinx.ext.autodoc',
            'sphinx.ext.napoleon'
]
```
> Para saber mais sobre docstrings você pode consultar alguns desses tutoriais em português: [caderno de laboratorio](https://cadernodelaboratorio.com.br/2017/05/31/documentando-um-programa-python-com-docstrings-e-pydoc/) e [python help](https://pythonhelp.wordpress.com/2011/02/14/docstrings/). 

* Os módulos (tests e simples) se encontram fora da pasta docs, então para eles serem reconhecidos é necessário especificar a sua localização.

```python
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../simples'))
sys.path.insert(0, os.path.abspath('../tests'))
```
* Para usar o template do _read the docs_ é necessário realizar a instalação do tema e por fim alterar a variável ``html_theme``.

No terminal:
```console
foo@bar:~/ pip install sphinx_rtd_theme
```
No arquivo ``conf.py``
```python
html_theme = 'sphinx_rtd_theme'
```

#### Modificando o ``index.rst``

No arquivo ``index.rst`` adicionar a seguinte linha ``source/modules``

```
    .. toctree::
    :maxdepth: 2
    :caption: Contents:

    source/modules
```

Por fim, para construir o html da sua documentação, execute o terminal o comando ``make html``

```console
foo@bar:~/simples/docs$ make html
```

O html será gerado dentro do caminho ``~/simples/docs/_build/html``. Você poderá visualizar a aplicação em ```http://localhost:8000/```, realizando os seguintes comandos.

```console
foo@bar:~/simples/docs$ cd _build/html
foo@bar:~/simples/docs/_build/html$ python -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

#### Referências

* [Sphinx for Python documentation ](https://gisellezeno.com/tutorials/sphinx-for-python-documentation.html)
* [First Steps with Sphinx](https://www.sphinx-doc.org/en/1.5/tutorial.html)
* [Getting Started with Sphinx](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html)

