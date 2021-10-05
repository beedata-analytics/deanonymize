import codecs
import csv
import os
import shutil
import subprocess
import unicodedata
from ast import parse


class DeanonymizeHTML(object):
    @staticmethod
    def replace_html(filename, data, delimiter, id, batch_text):
        """fix the contract name """

        def valid_variable_name(name):
            try:
                parse("{} = None".format(name))
                return name
            except Exception:
                # general case
                # new_name = hashlib.md5(name).hexdigest()
                # only considering the enercoop case
                new_name = name.replace("-", "_")
                return new_name

        """Replaces anonymized tokens in a given file with real data."""

        name = os.path.split(filename)[1]
        extension = os.path.splitext(filename)[1]
        new_name = "%s%s%s" % (name.split("~")[0], "-" + batch_text if batch_text is not None else "", extension)
        target = filename.replace(name, new_name)
        shutil.copyfile(filename, target)

        with codecs.open(data, mode="r", encoding="utf-8") as infile:
            csv_reader = csv.DictReader(infile, delimiter=delimiter)
            translations = {
                # avoiding special characters and replacing
                # blank spaces with '_'
                "%s_%s"
                % (
                    unicodedata.normalize("NFKD", cell)
                    .encode("ascii", "ignore")
                    .decode("ascii")
                    .replace(" ", "_"),
                    valid_variable_name(row[id]),
                ): row[cell]
                .encode("ascii", "xmlcharrefreplace")
                .decode("ascii")
                for row in csv_reader
                for cell in row.keys()
            }
            contract = valid_variable_name(
                os.path.basename(filename).split("~")[0]
            )

            translations = {
                k: translations[k] for k in translations if contract in k
            }

        for key in translations:
            subprocess.call(
                ["src/sed_replace.sh", key, translations[key], target],
            )

        return target
