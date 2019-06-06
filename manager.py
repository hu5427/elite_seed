from flask_migrate import MigrateCommand
from flask_script import Manager
from info import app, db

# 六 集成flask_script
manager = Manager(app)

# 七 集成flask_migrate
Manager(app, db)
manager.add_command("db", MigrateCommand)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    manager.run()
