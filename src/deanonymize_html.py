import string
import codecs
import csv


class DeanonymizeHTML(object):
    @staticmethod
    def replace_html(filename, data):
        """Replaces anonymized tokens in a given file with real data."""
        with open(data, mode="r", encoding="utf-8") as infile:
            csv_reader = csv.DictReader(infile)
            translations = {
                "%s_%s" % (cell, row["id"]): row[cell]
                for row in csv_reader
                for cell in row.keys()
            }

        with codecs.open(filename, "r", encoding="utf-8") as anonymized_html:
            anonymized_template = string.Template(anonymized_html.read())
            with open(filename.replace("~", "~deanonymized~"), "w") as outfile:
                outfile.write(
                    anonymized_template.safe_substitute(translations)
                )
        return outfile.name
