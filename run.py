''' Used to start flask application on terminal'''

from app import create_app

#create an instance of app called app.
app = create_app('development')

#run app when flask run is entered on terminal.
if __name__ == '__main__':
    app.run()