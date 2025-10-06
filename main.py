import webview
import win32print
import sys
import os
import configparser
import logging
from logger_config import setup_logging

# ------------------------------
# Utility Functions
# ------------------------------

def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for both development and PyInstaller builds.
    """
    if hasattr(sys, "_MEIPASS"):  # When running as a PyInstaller .exe
        base_path = sys._MEIPASS
        logging.debug(f"Running from PyInstaller bundle. Base path: {base_path}")
    else:
        base_path = os.path.abspath(".")
        logging.debug(f"Running in development mode. Base path: {base_path}")
    
    full_path = os.path.join(base_path, relative_path)
    logging.debug(f"Resolved resource path: {relative_path} -> {full_path}")
    return full_path


def load_config(path="config.properties") -> str:
    """
    Load web.url from a .properties file.
    Supports simple key=value format without sections.
    """
    logging.info(f"Loading configuration from: {path}")
    config_path = resource_path(path)
    logging.debug(f"Resolved config path: {config_path}")
    
    if not os.path.exists(config_path):
        logging.error(f"Configuration file not found: {config_path}")
        raise FileNotFoundError(f"Config file not found: {config_path}")

    try:
        config = configparser.ConfigParser()
        config.optionxform = str  # preserve case sensitivity
        
        logging.debug("Reading configuration file")
        with open(config_path, "r", encoding="utf-8") as f:
            content = "[DEFAULT]\n" + f.read()
        config.read_string(content)
        
        web_url = config["DEFAULT"].get("web.url", "").strip()
        if not web_url:
            logging.error("Missing required 'web.url' entry in config file")
            raise ValueError("Missing 'web.url' entry in config.properties")
            
        logging.info(f"Configuration loaded successfully. URL: {web_url[:30]}...")  # Log only first part of URL for privacy
        return web_url
        
    except (configparser.Error, IOError) as e:
        logging.error(f"Error parsing configuration file: {str(e)}", exc_info=True)
        raise


# ------------------------------
# Printer API
# ------------------------------

class PrinterApi:
    def list_printers(self):
        """
        Returns all installed printers and marks the default one.
        """
        logging.info("Listing available printers")
        printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        default_printer = win32print.GetDefaultPrinter()
        logging.info(f"Found {len(printers)} printers. Default: {default_printer}")
        return {"printers": printers, "default": default_printer}

    def print_text(self, printer_name, text):
        """
        Send raw text directly to the specified printer.
        """
        logging.info(f"Printing to {printer_name}")
        try:
            handle = win32print.OpenPrinter(printer_name)
            job = win32print.StartDocPrinter(handle, 1, ("Receipt", None, "RAW"))
            win32print.StartPagePrinter(handle)
            win32print.WritePrinter(handle, text.encode("utf-8"))
            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)
            win32print.ClosePrinter(handle)
            logging.info(f"Successfully printed to {printer_name}")
            return {"status": "success", "message": f"Printed on {printer_name}"}
        except Exception as e:
            logging.error(f"Print error on {printer_name}: {str(e)}", exc_info=True)
            return {"status": "error", "message": str(e)}


# ------------------------------
# Main Application
# ------------------------------

if __name__ == "__main__":
    try:
        # Initialize logging
        logger = setup_logging()
        logger.info("Starting Posterita Printer Utility")

        # Load URL from config.properties
        url = load_config()
        logger.info(f"Loading Web URL: {url}")

        api = PrinterApi()
        logger.info("Printer API initialized")

        # Create and launch pywebview window
        window = webview.create_window(
            "Posterita Printer Utility",
            url,
            js_api=api,
            text_select=True  # Allow text selection
        )
        logger.info("Window created, starting webview")

        webview.start(debug=True)
    except Exception as e:
        logging.error(f"Application error: {str(e)}", exc_info=True)
        # Use sys.stdin.readline() instead of input() for PyInstaller compatibility
        import msvcrt
        print("\nPress any key to exit...")
        msvcrt.getch()
