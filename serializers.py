from flask_restful.reqparse import RequestParser

#adicionar os serializers aqui

task_request_parser: RequestParser = RequestParser()
task_request_parser.add_argument('name', type=str, help='Campo obrigatório não preenchido', required=True)

funcao_serializer: RequestParser = RequestParser()
funcao_serializer.add_argument('descricao', type=str, help='Campo obrigatório não preenchido', required=True)
