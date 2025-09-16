from logging import INFO, getLogger, Formatter, StreamHandler
from os.path import join, exists, dirname, abspath
from logging.handlers import RotatingFileHandler
from os import makedirs

ENV = "development"

class LoggerService:
    """Telegram bot uchun rivojlangan log xizmati."""

    _instance = None  # Singleton uchun

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_file="app.log", log_level=INFO, max_bytes=1000000, backup_count=5, log_format=None):
        if hasattr(self, 'logger'):
            return  # Bir marta sozlash

        # ✅ Joriy fayl (core.py) joylashgan papka => LoggingService/
        base_dir = dirname(abspath(__file__))
        log_file_path = join(base_dir, log_file)

        # 📁 Papkani yaratish (agar mavjud bo‘lmasa)
        if not exists(base_dir):
            makedirs(base_dir)

        self.logger = getLogger("TurniketLogger")
        self.logger.setLevel(log_level)

        log_format = log_format or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = Formatter(log_format)

        handler = RotatingFileHandler(log_file_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
        handler.setLevel(log_level)
        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)

        # 🖥️ Konsolga log (faqat ishlab chiqishda)
        if ENV == "development":
            console_handler = StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        """Logger ob'ektini qaytaradi."""
        return self.logger

    def set_log_level(self, level):
        """Log darajasini sozlash funksiyasi."""
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    @staticmethod
    def log_exception(exc: Exception, message: str = "Exception occurred"):
        """Istisno hodisalarini logga yozish uchun yordamchi funksiyasi."""
        logger = LoggerService().get_logger()
        logger.error(f"{message}: {exc}", exc_info=True)

if __name__ == "__main__":
    log = LoggerService().logger
    log.info("✅ Logger muvaffaqiyatli ishga tushdi.")