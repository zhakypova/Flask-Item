from app import app
from app.models import *

if __name__ == '__main__':
    db.create_all()
    from app.urls import *
    app.run(debug=True)



