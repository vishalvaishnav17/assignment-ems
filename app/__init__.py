from flask import Flask, jsonify, send_from_directory
from app.config import Config
from app.database import db_session, init_db
from app.controllers.employee_controller import employee_bp
from app.utils.exceptions import ApplicationError


def create_app():
    """Application factory for configuring and instantiating the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database tables schema if they don't already exist
    init_db()

    # Register endpoints blueprint
    app.register_blueprint(employee_bp)

    # Teardown current db session after request completes to free up connection pools
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Global Exception Handlers mapping to standardized JSON payloads
    @app.errorhandler(ApplicationError)
    def handle_application_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def handle_internal_server_error(error):
        return jsonify({"error": "An unexpected internal server error occurred."}), 500

    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint for Docker container checks."""
        return jsonify({"status": "healthy"}), 200

    @app.route("/docs", methods=["GET"])
    def swagger_ui():
        """Serve Swagger UI page."""
        import os
        return send_from_directory(os.path.join(app.root_path, 'static'), 'swagger.html')

    return app
