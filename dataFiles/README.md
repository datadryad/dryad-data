Data Files
=================

This folder contains summary reports showing the distribution of bitstream formats across all items in Dryad's Data Files collection at the time the report was run.

## About the Data Files Report
The report shows counts for the known bitstream formats in Dryad's bitstream format registry (registry). The registry stores information about each of the formats, including MIME type, support level and a list of file extensions associated with the format. 

## How the Report is Generated
The report is generated using the profileformats task, which runs through the DSpace curation tasks system on Dryad's production server.

When the profileformats task is run, it reads the file extension of each bitstream currently in Dryad's Data Files collection, uses the file extension to look up the file format of the bitstream in the registry and updates the counts accordingly. The counts are then used to generate the report.
