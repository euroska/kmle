import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from doc_api.main import create_app, db
from doc_api.main.model import document
from doc_api import blueprint

app = create_app()
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command("db", MigrateCommand)


@manager.command
def run():
    app.run(host="0.0.0.0", port=5000)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover("doc_api/test", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
