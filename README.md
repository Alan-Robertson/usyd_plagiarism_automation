# Plagiarism Reporting Automation #

The plagiarisim reporting system seems pathologically designed to prevent automation. This repo provies a small fix for this using selenium.

## Usage ##
```bash
python plagiarism_report.py <data_csv>
```

After running the script you'll be presented with the login page; do this yourself (so I don't have to touch your credentials) and press enter on the script once you've finished with this.

The script should autofill the submission form. The script will not press the lodge button for you.

## CSV Format ##
See the sample csv provided.

## Unimplemented Features ##
The submission fails if more than 50 entries are passed in, at some point in the future I may automate splitting this up.


