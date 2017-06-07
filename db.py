from flask.ext.mysql import MySQL

mysql = MySQL()
def init_mysql(app):
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'cnl'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
