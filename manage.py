from app import create_app, mail, celery, sentry
from app.models import *

app = create_app(cf)

if __name__ == "__main__":
    app.run(port="8080")
