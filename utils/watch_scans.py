import os
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from PIL import Image

WATCH_FOLDER = r"E:\ClioScanToStaging"

class ScanHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith(".pdf"):
            return

        time.sleep(1)  # Give time for scan to finish writing

        print(f"[+] New file detected: {event.src_path}")
        try:
            pages = convert_from_path(event.src_path, first_page=1, last_page=1)
            pages = convert_from_path(event.src_path, first_page=1, last_page=1)
            if pages:
                barcode_data = self.extract_barcode(pages[0])
                if barcode_data:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
                    original_name = os.path.splitext(os.path.basename(event.src_path))[0]
                    new_name = f"{barcode_data} - {original_name} - {timestamp}.pdf"
                    new_path = os.path.join(os.path.dirname(event.src_path), new_name)
                    os.rename(event.src_path, new_path)
                    print(f"[✓] Renamed file: {new_path}")
                else:
                    print("[!] No barcode found.")

        except Exception as e:
            print(f"[ERROR] Failed to process {event.src_path}: {e}")

    def extract_barcode(self, image: Image.Image):
        barcodes = decode(image)
        for barcode in barcodes:
            return barcode.data.decode("utf-8")
        return None

if __name__ == "__main__":
    print(f"📁 Watching folder: {WATCH_FOLDER}")
    observer = Observer()
    observer.schedule(ScanHandler(), path=WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
