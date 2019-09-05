import string
import csv


class DeanonymizeHTML(object):

    @staticmethod
    def replace_html(filename, data):
        """Replaces anonymized tokens in a given file with real data."""
        with open(data, mode='r') as infile:
            reader = csv.reader(infile)
            translations = {rows[0]: rows[1] for rows in reader}
        with open(filename, 'r') as anonymized_html:
            anonymized_template = string.Template(anonymized_html.read())
            with open(filename.replace('~', '~deanonymized~'), 'w') as outfile:
                outfile.write(anonymized_template.safe_substitute(translations))
