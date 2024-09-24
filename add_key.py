import json
import sys
import os
import polib
from googletrans import Translator


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


def add_key(source_po_path, target_language, key, string, detail_string = ''):
    os.path.dirname(source_po_path)
    directory_path, filename = os.path.split(source_po_path)
    directory_path_no_locale = directory_path.rsplit('/', 1)[0]
    target_po_path =  directory_path_no_locale + "/" + target_language + "/" + filename
    if is_valid_language(target_language):
        translated_string = perform_translation(string, target_language)
        po_file = polib.pofile(target_po_path)
        new_entry = polib.POEntry(
            msgid=key,
            msgstr=translated_string
        )

        po_file.append(new_entry)
        po_file.save(target_po_path)
        progress_message = f"{detail_string} translated into {target_language} "
        print(progress_message)


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

        key = input("key: ")
        string = input("string: ")

        with open(locale_keys_file) as f:
            data = json.load(f)
            total_keys = len(data)

            for index, target_language in enumerate(data, start=1):
                detail_string = f"{index} out of {total_keys} locales."
                add_key(source_po_path, target_language, key, string, detail_string)




    if len(sys.argv) <2 or len(sys.argv) >3:
        print("Usage: python translate.py <source_file>")
        sys.exit(1)