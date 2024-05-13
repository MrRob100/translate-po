import sys
import os
import polib
from googletrans import Translator

def perform_translation(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)

    return translated.text


def translate_po_file(source_po_path, target_po_path, target_language):
    source_po = polib.pofile(source_po_path)

    target_directory = os.path.dirname(target_po_path)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    target_po = polib.POFile()

    target_po.metadata = {
        'Language': target_language,
    }

    total_entries = len(source_po)
    for index, entry in enumerate(source_po):
        translated_msgstr = perform_translation(entry.msgstr, target_language)
        new_entry = polib.POEntry(
            msgid=entry.msgid,
            msgstr=translated_msgstr
        )
        target_po.append(new_entry)
        completion_percentage = (index + 1) / total_entries * 100
        progress_message = f"{completion_percentage:.2f}% translated into {target_language}"
        print(progress_message, end='\r', flush=True)

    target_po.save(target_po_path)


def is_valid_language(target_language):
    translator = Translator()
    try:
        translation = translator.translate("test", dest=target_language)
        if not translation.text:
            print('translated false')
            sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python translate.py <source_file> <output_lang>")
        sys.exit(1)
    source_po_path = sys.argv[1]
    os.path.dirname(source_po_path)
    directory_path, filename = os.path.split(source_po_path)
    directory_path_no_locale = directory_path.rsplit('/', 1)[0]
    target_language = sys.argv[2]
    target_po_path =  directory_path_no_locale + "/" + target_language + "/" + filename
    is_valid_language(target_language)
    translate_po_file(source_po_path, target_po_path, target_language)
