from flask.ext.mysql import MySQL

mysql = MySQL()
def init_mysql(app):
    app.config['MYSQL_DATABASE_USER'] = 'cnl'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'cnl'
    app.config['MYSQL_DATABASE_DB'] = 'cnl'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
