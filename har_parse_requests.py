from harparser import HAR
import glob
import json
import os
import logging

def my_custom_logger(logger_name, level=logging.DEBUG):
    """
    Method to return a custom logger with the given name and level
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    format_string = ("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:"
                    "%(lineno)d — %(message)s")
    log_format = logging.Formatter(format_string)
    # Creating and adding the console handler
    console_handler = logging.StreamHandler(os.sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    # Creating and adding the file handler
    file_handler = logging.FileHandler(os.path.join('out', logger_name + '.log'), mode='a')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    return logger

def process_har(file_in):
    with open(file_in) as json_file:
        json_str = json.load(json_file)
        # Use key 'log' to match HAR standard
        my_har = HAR.log(json_str['log'])

        for entry in dict(my_har)['entries']:
            logger.info("REQUEST URL \n {}".format(dict(dict(entry)['request'])['url']))
            if 'postData' in dict(entry)['request']:
                logger.info("REQUEST DATA \n {}".format(dict(dict(entry)['request']['postData'])['text']))

            a, b, c, d = False, False, False, False
            for head in dict(dict(entry)['request'])['headers']:
                a = True if 'did' == dict(head)['name'] else False
                b = True if 'access_token' == dict(head)['name'] else False
                c = True if 't_token' == dict(head)['name'] else False
                d = True if 't_time' == dict(head)['name'] else False

            logger.info("REQUEST Headers include: did {} access token {} t_token {} t_time {}".format(a, b, c, d))
            if 'text' in dict(dict(entry)['response']['content']):
                logger.info("RESPONSE CONTENT \n {}".format(dict(dict(entry)['response']['content'])['text']))
            else:
                logger.info("RESPONSE CONTENT \n {}".format(dict(dict(entry)['response']['content'])))


if __name__ == "__main__":
    har_list = glob.glob(os.path.join('hars', '*.har'))
    for har_file in har_list:
        logger = my_custom_logger(os.path.basename(har_file))
        logger.info("Processing {}.".format(har_file))
        print("Processing {}.".format(har_file))
        process_har(har_file)
