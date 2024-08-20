import json
import sys
import os
import polib
from googletrans import Translator

def perform_translation(text, target_language):
    try:
        text = text[:5000]
        translator = Translator()
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        print(text + ':')
        print(e)
        return ''


def translate_po_file(source_po_path, target_language, detail_string = ''):
    os.path.dirname(source_po_path)
    directory_path, filename = os.path.split(source_po_path)
    directory_path_no_locale = directory_path.rsplit('/', 1)[0]
    target_po_path =  directory_path_no_locale + "/" + target_language + "/" + filename
    if is_valid_language(target_language):
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
            progress_message = f"{detail_string} {completion_percentage:.2f}% translated into {target_language} "
#             print(progress_message, end='\r')
            print(progress_message)

        target_po.save(target_po_path)


def is_valid_language(target_language):
    translator = Translator()
    try:
        translation = translator.translate("test", dest=target_language)
        if translation.text:
            return True
        else:
            print('translated false')
            return False
    except Exception as e:
        print(e)
        print(target_language)
        return False


if __name__ == "__main__":
    if len(sys.argv) == 2:
        source_po_path = sys.argv[1]
        ojs_version = input("OJS version: (eg 3.3 or 3.4. 3.3 uses country explicit locale keys eg 'en_US' whereas 3.4 and above uses just the language eg 'en') ")
        if ojs_version == '3.3':
            set = input("Which set of locale keys? 'full' or 'up' ")
            if set == 'all':
                locale_keys_file = 'keys/3.3/all.json'
            elif set == 'up':
                locale_keys_file = 'keys/3.3/up.json'
        elif ojs_version == '3.4' or '3.5':
            set = input("Which set of locale keys? 'full' or 'up' ")
            if set == 'all':
                locale_keys_file = 'keys/3.4/all.json'
            elif set == 'up':
                locale_keys_file = 'keys/3.4/up.json'
        else:
            print("Error: Invalid input. Please enter 3.3, 3.4, or 3.5.")
            sys.exit(1)

        with open(locale_keys_file) as f:
            data = json.load(f)
            total_keys = len(data)

            for index, target_language in enumerate(data, start=1):
                detail_string = f"{index} out of {total_keys} locales."
                translate_po_file(source_po_path, target_language, detail_string)


    if len(sys.argv) == 3:
        source_po_path = sys.argv[1]
        target_language = sys.argv[2]
        translate_po_file(source_po_path, target_language)

    if len(sys.argv) <2 or len(sys.argv) >3:
        print("Usage: python translate.py <source_file> <output_lang> leave output_lang blank for all locales")
        sys.exit(1)