from pathlib import Path

from .default_paths import PROJECT_FOLDERS

############################################################################################
def make_copyFromELABFTW_file(main_dir:Path):
    path = main_dir / PROJECT_FOLDERS.nb_exploration / "download_experiment_and_data_from_ELABFTW.ipynb"
    try:
        with open(path,"x") as f:
            f.write('''{
    "cells": [
    {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Download data from eLabFTW",
        "use this notebook to download data from eLabFTW.",
        "",
        "Add all the samples codes below to make it easier to download all the data.",
        ""
        ]
    },
    {
    "cell_type": "code",
    "execution_count": null,
    "metadata": {},
    "outputs": [],
    "source": [
        "from arenz_group_python import elabftw",
        ""
    ]
    },
    {
    "cell_type": "code",
    "execution_count": null,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Connect to eLabFTW",
        "Remember to set the environment variable ELABFTW_API_KEY to your API key in your .env-file.",
        "elabftw.connect()",
        "",
        ""
    ]
    },
    {
    "cell_type": "code",
    "execution_count": null,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Download a specific experiment and all related experiments and save it to the rawdata folder",
        "# The ID of the experiment can be found in the eLabFTW web interface", 
        "elabftw.download_experiment(ID)",
        "#where ID is a number, e.g. 1234 or hte name of the experiment, e.g. 'SPR-GW005'.",
        ""
    ]
    },
    {
    "cell_type": "code",
    "execution_count": null,
    "metadata": {},
    "outputs": [],
    "source": [
        "Dataset 2",
        "elabftw.download_experiment_tree('SPR-GW006')",
        "",
        ""
    ]
    },
    {
    "cell_type": "code",
    "execution_count": null,
    "metadata": {},
    "outputs": [],
    "source": [
        "Dataset 3",
        "elabftw.download_experiment_tree('SPR-GW007')",
        "",
        ""
    ]
    }
    ],
    "metadata": {
    "kernelspec": {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3"
    },
    "language_info": {
    "name": "python",
    "version": "3.11.5"
    }
    },
    "nbformat": 4,
    "nbformat_minor": 2
    }''')
            f.close()
        print(f"+\"{path.name}\" was created")
    except FileExistsError:
        print(f"-\"{path.name}\" already exists")   
    return