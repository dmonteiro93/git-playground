# Robô Coletor de Celulares

## Setup

Setup

O projeto utiliza Python 3 e mantém suas dependências no arquivo requirements.txt.

1. Entrar na pasta do projeto

A partir da pasta que contém o projeto, entre em:

cd celular_robo
2. Instalar as dependências

Execute:

py -m pip install -r requirements.txt

No Windows, o comando py é utilizado para executar o Python e o pip correspondente à instalação ativa.

3. Preparar o ambiente de testes

O projeto já possui a configuração necessária no pyproject.toml:

[tool.pytest.ini_options]
pythonpath = ["src"]

Por isso, não é necessário instalar o projeto com pip install -e .. Os testes devem ser executados a partir da raiz da pasta celular_robo.

Para verificar se o ambiente está funcionando corretamente:

pytest -v

Se os testes forem encontrados e executados, o ambiente está preparado.

## Como rodar

CLI

Para executar a interface de linha de comando, estando na raiz do projeto (celular_robo), utilize:

py -m celular_robo

Caso a CLI seja disponibilizada por um script específico do projeto, utilize o comando definido no arquivo de configuração correspondente.

Testes

Para executar toda a suíte de testes com informações detalhadas:

pytest -v

O comando deve ser executado na raiz do projeto, onde estão o pyproject.toml, requirements.txt, src/ e tests/.

Para executar apenas um arquivo de testes específico:

pytest -v tests/test_configuracao.py

Também é possível executar um teste específico utilizando seu nome:

pytest -v tests/test_configuracao.py -k nome_do_teste

## Decisões de projeto

## Decisões de projeto

### Validação de pedidos

A validação foi dividida entre **pedido** e **configuração** para manter responsabilidades separadas.

* `PedidoInvalido` é utilizado para problemas relacionados ao pedido, como:

  * pedido vazio;
  * codinome de celular inexistente no catálogo;
  * quantidade solicitada maior que a quantidade disponível;
  * conflito entre itens `frágeis` e `urgentes` no mesmo pedido, quando aplicável.

* `ConfiguracaoInvalida` é utilizada para problemas relacionados à configuração do robô, como:

  * estratégia incompatível com a área;
  * estratégia incompatível com as características configuradas;
  * configuração que não atende às regras da LPS.

### Conflito `fragil` + `urgente`

Foi decidido tratar o conflito entre `fragil=True` e `urgente=True` como **`PedidoInvalido`** quando as duas características são solicitadas para o mesmo item.

A decisão considera que o conflito representa uma incompatibilidade nas características do pedido, e não um erro na configuração geral do robô.

As regras individuais permanecem:

* pedido urgente → `RotaDireta`;
* pedido frágil → `RotaComDuplaConferencia`.

Como essas estratégias são incompatíveis entre si para o mesmo item, a combinação é rejeitada.

### Catálogo de disponibilidade

O catálogo mantém somente os **codinomes dos celulares e suas respectivas quantidades disponíveis**.

Ele é utilizado pela validação do pedido para verificar:

1. se o codinome existe;
2. se a quantidade solicitada está disponível.

A quantidade coletada não pode ficar negativa nem ultrapassar a quantidade solicitada para aquele pedido.

### Descriptor `QuantidadeValida`

Foi utilizado um descriptor para centralizar a validação da quantidade coletada.

Diferentemente de um limite fixo arbitrário, a validação deve considerar o limite estabelecido pelo pedido: a quantidade coletada deve permanecer entre `0` e a quantidade solicitada.

### Registro de rotas

As estratégias de rota possuem seu próprio mecanismo de registro por meio de `RotaColeta.__init_subclass__` e `_registro_rotas`.

A lista `ESTRATEGIAS_VALIDAS` é derivada desse registro. Dessa forma, o conjunto de estratégias aceitas pela configuração é definido pelas subclasses de `RotaColeta`, sem depender da hierarquia `Estrategia` utilizada em outros exemplos da disciplina.

### Factory

A criação dos robôs utiliza o registro de subclasses mantido por `Robo`.

A factory recebe o nome do tipo e instancia a classe correspondente, evitando a necessidade de uma sequência de `if/elif` para cada tipo de robô.

A criação de um robô configurado também realiza a validação da configuração antes de aplicar a configuração ao robô.

### State

O comportamento do robô durante o processo de coleta foi dividido em estados:

* `ModoColetando`: permite a execução das coletas;
* `ModoAguardandoVerificacao`: bloqueia novas coletas enquanto a bandeja aguarda verificação.

Quando a bandeja fica completa, o robô passa para o estado de espera. Caso o pedido seja rejeitado, retorna ao modo de coleta, mantendo os itens que já haviam sido coletados.

### Command

Cada operação de coleta é representada por `ComandoColeta`.

O comando possui `execute()` para realizar a coleta e `desfazer()` para revertê-la. Isso permite desfazer uma operação sem precisar duplicar a lógica de alteração da bandeja em diferentes partes do sistema.

### Observer

O padrão Observer foi utilizado para desacoplar os eventos do robô das ações realizadas em resposta a eles.

* `EquipeDeTestes` reage ao evento de bandeja pronta;
* `RegistroAuditoria` registra os eventos relevantes do sistema, incluindo coletas, bandeja pronta e pedidos rejeitados.

### LPS e configuração

As configurações possíveis são validadas de acordo com as regras da linha de produtos:

* `centro_padrao` → não possui obstáculos;
* `area_quarentena` → possui pelo menos uma posição bloqueada;
* `urgente=True` → exige `RotaDireta`;
* `fragil=True` → exige `RotaComDuplaConferencia`;
* `area_quarentena` → não permite `RotaDireta`.

As incompatibilidades de configuração são tratadas como `ConfiguracaoInvalida`.

### Persistência

Os dados fornecidos pelo projeto são mantidos em arquivos de dados separados do código-fonte, permitindo que o catálogo e demais informações persistidas sejam carregados sem precisar alterar as classes responsáveis pela lógica do robô.


## Mapeamento pra aulas da disciplina

Descriptors
robo_coletor.py — QuantidadeValida
Validação da quantidade coletada, respeitando os limites do pedido.

__init_subclass__
robo_base.py — Robo
Registro automático das subclasses de robô utilizado pela Factory.

__init_subclass__
robo_coletor.py — RotaColeta
Registro automático das estratégias de rota.

Strategy
robo_coletor.py — RotaColeta, RotaDireta, RotaComDuplaConferencia
Encapsula diferentes formas de realizar a rota de coleta.

Command
robo_coletor.py — ComandoColeta
Encapsula uma operação de coleta e permite executá-la e desfazê-la.

Factory
robo_coletor.py — criar_robo_coletor, criar_robo_configurado
Cria robôs a partir do tipo registrado e valida configurações.

Observer
robo_coletor.py — EquipeDeTestes, RegistroAuditoria
Reação aos eventos do robô e registro das operações realizadas.

State
robo_coletor.py — ModoColetando, ModoAguardandoVerificacao
Altera o comportamento do robô conforme o estado da bandeja/verificação.

LPS
configuracao.py / robo_coletor.py
Regras de configuração para centro_padrao, area_quarentena, urgente e fragil.

Exceções
excecoes.py
ErroColeta, ConfiguracaoInvalida e PedidoInvalido.

Persistência
dados/ + módulos de carregamento
Armazenamento e carregamento do catálogo de celulares e quantidades disponíveis.

Testes
tests/
Testes automatizados das configurações, pedidos e fluxos completos do sistema.