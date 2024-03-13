from flask import Flask, jsonify
from app.jobs.MailSender import MailSender
from app.routes.AuthRoutes import auth
from app.routes.UserRoutes import users, adminUsers
from app.routes.TrainingProgramRoutes import trainingPrograms
from app.routes.TrainingsRoutes import trainings


app = Flask(__name__)

def init_app():

    # Health check
    @app.route('/', methods=['GET'])
    def health():
        return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

    app.mail_sender = MailSender()

    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(adminUsers)
    app.register_blueprint(trainingPrograms)
    app.register_blueprint(trainings)

    return app