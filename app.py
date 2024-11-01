from src.setup import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host=app.config["FLASK_HOST"],
        port=int(app.config["FLASK_PORT"]),
        debug=app.config["FLASK_DEBUG"] == "True",
        load_dotenv=False,
    )
