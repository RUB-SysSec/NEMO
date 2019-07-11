from logging.handlers import RotatingFileHandler
import multiprocessing, threading, logging, sys, traceback
from rainbow_logging_handler import RainbowLoggingHandler # pip install rainbow_logging_handler

class MultiProcessingLog(logging.Handler):
    def __init__(self, name, mode, maxsize, rotate):
        logging.Handler.__init__(self)

        #self._handler = RotatingFileHandler(name, mode, maxsize, rotate)
        formatter = logging.Formatter("[%(asctime)s.%(msecs)03d] %(filename)16s Line %(lineno)3d %(funcName)s():\t %(message)s")
        self._handler = RainbowLoggingHandler(sys.stderr, color_funcName=('green', 'none', True))
        self._handler.setFormatter(formatter)

        self.queue = multiprocessing.Queue(-1)

        t = threading.Thread(target=self.receive)
        t.daemon = True
        t.start()

    def setFormatter(self, fmt):
        logging.Handler.setFormatter(self, fmt)
        self._handler.setFormatter(fmt)

    def receive(self):
        while True:
            try:
                record = self.queue.get()
                self._handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)

    def send(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        # ensure that exc_info and args
        # have been stringified.  Removes any chance of
        # unpickleable things inside and possibly reduces
        # message size sent over the pipe
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            dummy = self.format(record)
            record.exc_info = None

        return record

    def emit(self, record):
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        self._handler.close()
        logging.Handler.close(self)