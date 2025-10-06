import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

def setup_logging():
    """
    Configure logging with both file and console handlers.
    File logs will be stored in %APPDATA%/PosteritaPrinterUtility/logs/
    """
    # Create logs directory in AppData
    app_data = os.getenv('APPDATA')
    log_dir = Path(app_data) / "PosteritaPrinterUtility" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create a log file with timestamp
    log_file = log_dir / f"printer_utility_{datetime.now().strftime('%Y%m%d')}.log"

    # Set up logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(message)s'  # Simpler format for console
    ))

    # Get the root logger and add handlers
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info("Logging initialized")
    logging.info(f"Log file: {log_file}")

    return logger