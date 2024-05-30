# trabalho2-bd2-backend
Este será o repositório de armazenamento dos códigos para o backend do trabalho 2 da disciplina Banco de Dados 2 

## Organização dos arquivos
Os arquivos foram organizados de maneira a deixar o projeto o mais simples possível:

- **api.py**: Aqui está a raiz do nosso projeto, é onde se encontra as <u>urls</u> e a por onde inicia-se a <u>API</u>.
- **views.py**: É onde se encontra as classes que representam as Views do projeto, cada uma com seus métodos de GET, POST, PATCH e DELETE.
- **serializers.py**: Onde estão os serializadores para os métodos POST e PATCH do nosso projeto, um serializador basicamente vai dizer quais campos podem/vão vir na requisição.
- **dicts.py**: É onde estão os TypedDicts da API, eles servem para dizer melhor qual é o tipo necessário para criar/editar algo usando o método POST ou o método PATCH da nossa API.
- **validators.py**: Aqui se encontra os validadores da API, serve para verificar se os dados vindos de uma requisição POST/PATCH são válidos para ser colocados no Banco ou não.
- **models.py**: É onde se encontra a configuração do banco de dados da nossa aplicação, aqui está a criação das tabelas e a conexão com o banco em si.
- **utils.py**: Assim como todo arquivo de utils, esse serve para guardar funções que fazem de tudo que é coisa, e não se encaixam nos outros arquivos.
