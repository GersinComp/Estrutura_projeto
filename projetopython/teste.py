# from projetopython import app, database
# from projetopython.models import Usuario, Post
#
# with app.app_context():
#     database.create_all()
#
# with app.app_context():
#     usuario = Usuario(username='Lira', email='lira@gmail.com', senha='123456')
#     usuario2 = Usuario(username='Gerson', email='gerson@gmail.com', senha='123456')
#     database.session.add(usuario)
#     database.session.add(usuario2)
#     database.session.commit()
#
# with app.app_context():
#     meus_usuarios = Usuario.query.all()
#     print(meus_usuarios)
#     primeiro_usuario = Usuario.query.first()
#     print(primeiro_usuario)
#     print(primeiro_usuario.id)
#     print(primeiro_usuario.email)
#     print(primeiro_usuario.username)
#     # print(primeiro_usuario.data_criacao)
#     print(primeiro_usuario.posts)
#     print(primeiro_usuario.cursos)
#
#
#
