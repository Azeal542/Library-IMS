import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='application.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig()

def error_log(user, message):
    logger.error(user + " had an error: " + message)

def checkout_log(user, message):
    logger.info(user + " checked out: " + message)

def checkin_log(user, message):
    logger.info(user + " checked in: " + message)

def signin_log(user):
    logger.info(user + " signed in.")

def failed_login_log():
    logger.warning("Failed login attempt detected.")

def damaged_book_log(user, book):
    logger.warning(user + " reported a damaged book: " + book)


#user = "John Doe"
#error_log(user, "This is an error message.")
#checkout_log(user, "example book.")
#checkin_log(user, "example book.")
#signin_log(user)
#failed_login_log()