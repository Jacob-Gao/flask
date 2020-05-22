from pro_flask import create_app


app = create_app('settings.Config')
app.run(host='0.0.0.0')

