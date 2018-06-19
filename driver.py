import os

from app import App, logger


def main(app_directory):

    
    App(app_directory)


if __name__ == '__main__': 
    app_directory = os.path.dirname(os.path.realpath(__file__))

    # Try to run application. Otherwise log error.
    log = logger.Logger(app_directory, 'w')
    try:   
        main(app_directory)
    except:       
        log.createLog('')
