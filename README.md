# Geneticheck - UofTHacks2022
Project for UofTHacks 2022

Initial Project challenge:

In Varient’s mission to link people with rare diseases to treatment information for their
specific condition, we discovered that the information gap among the rare disease
community is, in part, caused by the lack of information standardization in the industry. With
each hospital, clinic, and genetic testing agency documenting their data differently, one
person’s genetic report can look miles apart from the other, making it inefficient to extract
meaningful information.

## Installation

This project was developed in Windows and Python 3.9.10, and thus Windows is required to run the scripts. Ensure Google Cloud is installed on the Windows Machine, initialized, and the API key JSON file is set as an enviroment variable

Then, setup the project enviroment

```
git clone https://github.com/not-cosmo/Geneticheck.git
cd Geneticheck
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
# Getting Started

To run the Genetic Report Image Detection, simply run `python geneDetection_gcloud.py`. This script outputs the detection PASS/FAIL of the Gene in the filename and creates an image copy with a bouding box of all Gene instances.

An opensource alternative was also written, however does not acheive the 100% accuracy the Google Cloud method achieves: `python geneDetection_pytesseract.py`
