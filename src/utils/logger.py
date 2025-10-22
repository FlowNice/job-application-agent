"""
Логирование и мониторинг (Logging and Monitoring Module)

Этот модуль предоставляет централизованное логирование (centralized logging)
для всех компонентов агента.
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

class LoggerSetup:
    """
    Класс для настройки логирования (Logger setup class)
    """
    
    _logger = None
    
    @staticmethod
    def get_logger(name: str = "JobApplicationAgent") -> logging.Logger:
        """
        Получить или создать логгер (Get or create logger)
        
        Args:
            name (str): Имя логгера (Logger name)
            
        Returns:
            logging.Logger: Объект логгера (Logger object)
        """
        if LoggerSetup._logger is not None:
            return LoggerSetup._logger
        
        # Создать директорию для логов, если её нет (Create logs directory if it doesn't exist)
        log_dir = Path("./logs")
        log_dir.mkdir(exist_ok=True)
        
        # Создать логгер (Create logger)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # Формат логирования (Logging format)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Обработчик для файла (File handler)
        log_file = log_dir / f"agent_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Обработчик для консоли (Console handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        LoggerSetup._logger = logger
        return logger


def get_logger(name: str = "JobApplicationAgent") -> logging.Logger:
    """
    Удобная функция для получения логгера (Convenience function to get logger)
    
    Args:
        name (str): Имя логгера (Logger name)
        
    Returns:
        logging.Logger: Объект логгера (Logger object)
    """
    return LoggerSetup.get_logger(name)


# Пример использования (Example usage)
if __name__ == "__main__":
    logger = get_logger("TestLogger")
    
    logger.debug("Это сообщение отладки (This is a debug message)")
    logger.info("Это информационное сообщение (This is an info message)")
    logger.warning("Это предупреждение (This is a warning message)")
    logger.error("Это сообщение об ошибке (This is an error message)")
    logger.critical("Это критическое сообщение (This is a critical message)")

