import logging

logging.basicConfig(
    filename='log.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


logging.debug('debug')
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')