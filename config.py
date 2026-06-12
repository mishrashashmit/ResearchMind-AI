import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


class Config:
    """Central configuration management for ResearchMind AI.
    
    Loads environment variables, sets up logging, defines paths,
    and provides API configuration.
    """
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GOOGLE_MODEL = "gemini-2.5-flash"
    
    BASE_DIR: Path = Path(__file__).resolve().parent
    OUTPUTS_DIR: Path = BASE_DIR / "outputs"
    REPORTS_DIR: Path = OUTPUTS_DIR / "reports"
    LOGS_DIR: Path = OUTPUTS_DIR / "logs"
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE: Path = LOGS_DIR / "researchmind.log"
    
    MAX_PAPERS_PER_SEARCH: int = 10
    SUMMARY_MAX_TOKENS: int = 500
    TIMEOUT_SECONDS: int = 30
    
    @staticmethod
    def validate_config() -> None:
        """Validate that required configuration is set.
        
        Raises:
            ValueError: If GEMINI_API_KEY is not set.
        """
        if not Config.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not set. Add it to .env file or set environment variable."
            )
    
    @staticmethod
    def ensure_directories() -> None:
        """Create necessary directories if they don't exist."""
        Config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> logging.Logger:
    """Set up logging configuration for the application.
    
    Creates a logger with both file and console handlers.
    File logs go to outputs/logs/researchmind.log
    Console logs appear in the terminal.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    Config.ensure_directories()
    
    logger = logging.getLogger("researchmind")
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    if logger.hasHandlers():
        return logger
    
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logging()
Config.ensure_directories()


if __name__ == "__main__":
    logger.info("Config module loaded successfully")
    logger.info(f"Using Google Model: {Config.GOOGLE_MODEL}")
    logger.info(f"Reports directory: {Config.REPORTS_DIR}")
    logger.info(f"Logs directory: {Config.LOGS_DIR}")
