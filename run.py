from app import create_app

app = create_app()

if __name__ == '__main__':
    # In a development environment, debug=True is useful.
    # For production, use a WSGI server like Gunicorn or uWSGI.
    app.run(debug=True, host='0.0.0.0', port=5000)
