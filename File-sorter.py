import os
import shutil
import argparse
import json
import logging
import threading
from pathlib import Path
from tkinter import Tk, filedialog, messagebox
from tqdm import tqdm

# پیش‌فرض دسته‌بندی پسوندها
EXT_CATEGORIES = {    

#-----------------------------------------------------------------------------------------------------------------------

    'Pictures': 

    ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.raw'],



#-----------------------------------------------------------------------------------------------------------------------

    'Music':

      ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.opus'],


#-----------------------------------------------------------------------------------------------------------------------

    'Videos': 
    
    ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.mpeg', '.mpg'],


#-----------------------------------------------------------------------------------------------------------------------

    'Documents': 
    
    ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf', '.txt', '.rtf', '.odt', '.csv', '.md'],


#-----------------------------------------------------------------------------------------------------------------------

    'Archives': 
    
    ['.zip', '.rar', '.tar', '.gz', '.7z', '.xz', '.iso'],



#-----------------------------------------------------------------------------------------------------------------------

    'Web': 
    
    
    ['.html', '.htm', '.css', '.js', '.json', '.xml', '.php', '.asp', '.jsp'],



#-----------------------------------------------------------------------------------------------------------------------

    'Code': 
    
    
    ['.py', '.java', '.cpp', '.c', '.rb', '.go', '.swift', '.js', '.ts', '.cs'],


#-----------------------------------------------------------------------------------------------------------------------

    'Fonts': 
    
    ['.ttf', '.otf', '.woff', '.woff2'],


#-----------------------------------------------------------------------------------------------------------------------

    'Executables':
     
      ['.exe', '.msi', '.apk'],

#-----------------------------------------------------------------------------------------------------------------------

    'Databases': 
    
    ['.db', '.sqlite', '.sql'],


#-----------------------------------------------------------------------------------------------------------------------
    'Text': 
    
    
    ['.log', '.ini', '.yaml', '.yml'],
}

# بارگذاری پیکربندی اضافی از فایل JSON
CONFIG_FILE = 'file_organizer_config.json'

# تنظیمات لاگ
logging.basicConfig(
    filename='file_organizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def load_config():
    if Path(CONFIG_FILE).is_file():
        try:
            data = json.loads(Path(CONFIG_FILE).read_text(encoding='utf-8'))
            EXT_CATEGORIES.update(data.get('categories', {}))
            logging.info('Config loaded from %s', CONFIG_FILE)
        except Exception as e:
            logging.error('Failed loading config: %s', e)


def build_lookup():
    lookup = {}
    for category, exts in EXT_CATEGORIES.items():
        for ext in exts:
            lookup[ext.lower()] = category
    return lookup


def organize_folder(source: Path, dest: Path, recursive=False, dry_run=False):
    lookup = build_lookup()
    stats = {}
    files = list(source.rglob('*') if recursive else source.iterdir())
    total = sum(1 for f in files if f.is_file())

    pbar = tqdm([f for f in files if f.is_file()], desc='Organizing', unit='file')
    for item in pbar:
        ext = item.suffix.lower()
        category = lookup.get(ext, 'Unknown')
        target_dir = dest / category
        if not target_dir.exists() and not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / item.name
        try:
            if not dry_run:
                shutil.move(str(item), str(target_path))
            stats[category] = stats.get(category, 0) + 1
            pbar.set_postfix({'Last': item.name})
            logging.info('Moved %s -> %s', item, target_path)
        except Exception as e:
            logging.error('Error moving %s: %s', item, e)
    return stats


def pick_folder(title):
    root = Tk()
    root.withdraw()
    path = filedialog.askdirectory(title=title)
    root.destroy()
    return Path(path) if path else None


def main():
    load_config()
    parser = argparse.ArgumentParser(description='Organize files into categorized folders.')
    parser.add_argument('-s', '--source', type=Path, help='مبدا (اگر خالی باشد، پنجره انتخاب گرافیکی باز می‌شود)')
    parser.add_argument('-d', '--dest', type=Path, help='مقصد (در صورت خالی، در کنار مبدا ساخته می‌شود)')
    parser.add_argument('-r', '--recursive', action='store_true', help='جستجوی بازگشتی در زیرپوشه‌ها')
    parser.add_argument('--dry-run', action='store_true', help='شبیه‌سازی عملیات بدون انتقال')
    args = parser.parse_args()

    source = args.source or pick_folder('Select Source Folder')
    if not source or not source.is_dir():
        messagebox.showerror('خطا', 'مسیر مبدا معتبر نیست!')
        return

    dest = args.dest or pick_folder('Select Destination Folder')
    if not dest:
        dest = source.parent / (source.name + '_organized')

    stats = {}
    # اجرای در رشته جدا برای نریختن UI
    thread = threading.Thread(
        target=lambda: stats.update(organize_folder(source, dest, args.recursive, args.dry_run)),
        daemon=True
    )
    thread.start()
    thread.join()

    summary = '\n'.join([f"{cat}: {cnt} files" for cat, cnt in stats.items()]) or 'هیچ فایلی منتقل نشد.'
    messagebox.showinfo('خلاصه', summary)
    print('Summary:')
    print(summary)

if __name__ == '__main__':
    main()