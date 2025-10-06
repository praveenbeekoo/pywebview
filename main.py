import webview
import win32print
import sys
import os
import configparser

# ------------------------------
# Utility Functions
# ------------------------------

def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for both development and PyInstaller builds.
    """
    if hasattr(sys, "_MEIPASS"):  # When running as a PyInstaller .exe
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_config(path="config.properties") -> str:
    """
    Load web.url from a .properties file.
    Supports simple key=value format without sections.
    """
    config_path = resource_path(path)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = configparser.ConfigParser()
    config.optionxform = str  # preserve case sensitivity
    with open(config_path, "r", encoding="utf-8") as f:
        content = "[DEFAULT]\n" + f.read()
    config.read_string(content)

    web_url = config["DEFAULT"].get("web.url", "").strip()
    if not web_url:
        raise ValueError("Missing 'web.url' entry in config.properties")
    return web_url


# ------------------------------
# Printer API
# ------------------------------

class PrinterApi:
    def list_printers(self):
        """
        Returns all installed printers and marks the default one.
        """
        printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        default_printer = win32print.GetDefaultPrinter()
        return {"printers": printers, "default": default_printer}

    def print_text(self, printer_name, text):
        """
        Send raw text directly to the specified printer.
        """
        try:
            handle = win32print.OpenPrinter(printer_name)
            job = win32print.StartDocPrinter(handle, 1, ("Receipt", None, "RAW"))
            win32print.StartPagePrinter(handle)
            win32print.WritePrinter(handle, text.encode("utf-8"))
            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)
            win32print.ClosePrinter(handle)
            return {"status": "success", "message": f"Printed on {printer_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


# ------------------------------
# Main Application
# ------------------------------

if __name__ == "__main__":
    try:
        # Load URL from config.properties
        url = load_config()
        print(f"[INFO] Loading Web URL: {url}")

        api = PrinterApi()

        # Create and launch pywebview window
        window = webview.create_window(
            "Posterita Printer Utility",
            url,
            js_api=api,
            confirm_quit=False,
            allow_url_access=True
        )

        webview.start()
    except Exception as e:
        print(f"[ERROR] {e}")
        input("Press Enter to exit...")
