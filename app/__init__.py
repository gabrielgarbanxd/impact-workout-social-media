from flask import Flask, jsonify
from app.jobs.MailSender import MailSender
from app.routes.AuthRoutes import auth


app = Flask(__name__)

def init_app():

    # Health check
    @app.route('/', methods=['GET'])
    def health():
        return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

    app.mail_sender = MailSender()

    app.register_blueprint(auth)

    return app