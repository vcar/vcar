from main import create_app

# create application instance
app = create_app()

if __name__ == '__main__':
    app.run(threaded=True)
