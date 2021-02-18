import itertools
import json
import os
from multiprocessing import Pool

import click
from deanonymize_html import DeanonymizeHTML
from tqdm import tqdm
from utils_report import UtilsReport


def deanonymize_report(
    report, data, layout, output_dir, delimiter, id, batch_text
):
    """Deanonymize report and convert it to PDF."""
    output_filename = DeanonymizeHTML.replace_html(
        report, data, delimiter, id, batch_text
    )
    with open(layout) as json_file:
        UtilsReport.write_pdf_landscape(
            output_filename, json.load(json_file), output_dir
        )
    os.remove(output_filename)


@click.command()
@click.option(
    "--data", type=click.Path(exists=True), help="Deanonymized data filename"
)
@click.option("--layout", type=click.Path(exists=True), help="PDF layout")
@click.option(
    "--report",
    type=click.Path(exists=True),
    help="Report file or directory name",
)
@click.option(
    "--output",
    type=click.Path(exists=True),
    help="Output directory",
)
@click.option(
    "--delimiter",
    type=click.STRING,
    default=",",
    help="Delimiter in the data filename, default value ',' ",
)
@click.option(
    "--id",
    type=click.STRING,
    default="id",
    help="Identifier in the data filename",
)
@click.option(
    "--batch-month",
    type=click.INT,
    help="Batch month to be included in the filename",
)
@click.option(
    "--batch-number",
    type=click.INT,
    help="Batch number to be included in the filename",
)
@click.option("--processes", default=16, type=click.INT)
def run(
    data,
    layout,
    report,
    output,
    delimiter,
    id,
    batch_month,
    batch_number,
    processes,
):
    if not os.path.exists(output):
        print("Output directory %s created" % output)
        os.mkdir(output)

    if os.path.isdir(report):
        onlyfiles = [
            os.path.join(report, f)
            for f in os.listdir(report)
            if os.path.isfile(os.path.join(report, f))
        ]
        docs = list(
            itertools.product(
                onlyfiles,
                [data],
                [layout],
                [output],
                [delimiter],
                [id],
                [batch_month],
                [batch_number],
            )
        )

        if processes > 1:
            pool = Pool(processes=processes)
            with tqdm(total=len(docs)) as pbar:
                for result in pool.imap_unordered(
                    func=deanonymize, iterable=docs
                ):
                    pbar.update()
        else:
            with tqdm(total=len(docs)) as pbar:
                for doc in docs:
                    deanonymize(doc)
                    pbar.update()

    if os.path.isfile(report):
        deanonymize_report(
            report,
            data,
            layout,
            output,
            delimiter,
            id,
            str(batch_month) + "-" + str(batch_number),
        )


def deanonymize(contract):
    (
        report,
        data,
        layout,
        output,
        delimiter,
        id,
        batch_month,
        batch_number,
    ) = contract
    deanonymize_report(
        report,
        data,
        layout,
        output,
        delimiter,
        id,
        str(batch_month) + "-" + str(batch_number),
    )


if __name__ == "__main__":
    run()
