from alayatodo import app
from .views.auth import auth
from .views.todo import todo
from .views.home import home

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(todo)




