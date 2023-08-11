import os
import shutil
import subprocess
from utils_report import UtilsReport

class DeanonymizeHTML(object):

    @staticmethod
    def get_filename(filename, batch_text):
        name = os.path.split(filename)[1]
        extension = os.path.splitext(filename)[1]
        new_name = "%s%s%s" % (name.split("~")[0], "-" + batch_text if batch_text is not None else "", extension)
        return filename.replace(name, new_name)


    @staticmethod
    def replace_html(filename, target, data):
        """fix the contract name """

        """Replaces anonymized tokens in a given file with real data."""

        shutil.copyfile(filename, target)

        contract = UtilsReport.valid_variable_name(
            os.path.basename(filename).split("~")[0]
        )

        translations = data.get(contract)

        for key in translations:
            subprocess.call(
                ["src/sed_replace.sh", key, translations[key], target],
            )

        return target
