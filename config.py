SECRET_KEY = 'genshin' 

#configuração de conexão com o db
SQLALCHEMY_DATABASE_URI = \
    "{SGBD}://{user}:{password}@{server}/{database}".format(
        SGBD = "mysql+mysqlconnector",
        user = "root",
        password = "root",
        server = "localhost",
        database = "jogoteca"
    )