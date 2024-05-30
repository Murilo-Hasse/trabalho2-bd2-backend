from flask_restful.reqparse import RequestParser

#adicionar os serializers aqui

funcao_serializer: RequestParser = RequestParser()
funcao_serializer.add_argument('descricao', type=str, help='Campo obrigatório não preenchido', required=True)
