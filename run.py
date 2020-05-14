from pro_flask import create_app


if __name__ == '__main__':
    app = create_app('settings.Config')
    app.run(host='0.0.0.0')

