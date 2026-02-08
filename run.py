from web import criar_app
from web.extensoes import db

app = criar_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
