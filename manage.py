from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager
from info import create_app, db
from info.models import *

# 调用create_app函数将配置类传入函数
app = create_app("development")
# 六 集成flask_script
manager = Manager(app)

# 七 集成flask_migrate
Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
