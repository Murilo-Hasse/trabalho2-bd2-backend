from flask_restful.reqparse import RequestParser

#adicionar os serializers aqui

task_request_parser: RequestParser = RequestParser()
task_request_parser.add_argument('name', type=str, help='Campo obrigatório não preenchido', required=True)
