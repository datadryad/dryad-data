#!/usr/bin/env python

"""
Reports shopping cart items in archive and publication blackout with payment dates in date range.

Example: To run the program from the command line:  
    $ python monthlyReportNew.py -s 2017-03-01 -e 2017-03-31

    Args:
        -s: start date for the report
        -e: end date for the report
    Output: Running the report results in a CSV file called monthlyReport.csv in the current directory
    Raises: ValueError for invalid date

Output: Running the report results in a CSV file called monthlyReport.csv in the current directory
"""

__author__ = "Debra Fagan"
__credits__ = ["Daisie Huang", "Ryan Scherle"]


import re
import os
import sys
import shutil
import hashlib
from datetime import datetime
import argparse


def dict_from_query(sql):
    # Now execute it
    cmd = "psql -A -U dryad_app dryad_repo -c \"%s\"" % sql
    output = [line.strip().split('|') for line in os.popen(cmd).readlines()]
    if len(output) <= 2: # the output should have at least 3 lines: header, body rows, number of rows
        return {}
    else:
        return dict(zip(output[0],output[1]))

def rows_from_query(sql):
    # Now execute it
    cmd = "psql -A -U dryad_app dryad_repo -c \"%s\"" % sql
    output = [line.strip().split('|') for line in os.popen(cmd).readlines()]
    if len(output) <= 2: # the output should have at least 3 lines: header, body rows, number of rows
        return None
    else:
        return output

def get_field_id(name):
    parts = re.split('\.', name)
    schema = dict_from_query("select metadata_schema_id from metadataschemaregistry where short_id = '%s'" % parts[0])['metadata_schema_id']
    if len(parts) > 2:
        field_id = dict_from_query("select metadata_field_id from metadatafieldregistry where metadata_schema_id=%s and element='%s' and qualifier = '%s'" % (schema, parts[1], parts[2]))['metadata_field_id']
    else:
        field_id = dict_from_query("select metadata_field_id from metadatafieldregistry where metadata_schema_id=%s and element='%s' and qualifier is null" % (schema, parts[1]))['metadata_field_id']
    return field_id

def build_output_string(item, labels):
    # Get values from previous shopping cart query
    item_id = item[labels['item']]
    cart_id = item[labels['cart_id']]
    expiration = item[labels['expiration']]
    status = item[labels['status']]
    depositor = item[labels['depositor']]
    currency = item[labels['currency']]
    country = item[labels['country']]
    voucher = item[labels['voucher']]
    total = item[labels['total']]
    transaction_id = item[labels['transaction_id']]
    journal = item[labels['journal']]
    journal_sub = item[labels['journal_sub']]
    order_date = item[labels['order_date']]
    payment_date = item[labels['payment_date']]
    notes = item[labels['notes']]
    last_mod_date = query_for_last_mod_date (item_id)
    archive_date  = query_for_archive_date (item_id)
    doi = query_for_doi (item_id)
    output_string = '\t'.join([cart_id, expiration, status, depositor, item_id, doi, currency, country, voucher, total, transaction_id, journal, journal_sub, order_date, payment_date, notes, last_mod_date, archive_date])
    return output_string

def query_for_last_mod_date (item_id):
    # Query database for the item's last_mod_date and return as string
    last_mod_date = dict_from_query("select last_modified from item where item_id = %s" % (item_id))['last_modified']
    return last_mod_date

def query_for_archive_date (item_id):
    # Query database for the item's archive_date and return as string if found; if not found, return string 'PBO'
    archive_date = 'PBO'
    is_archived = dict_from_query("select in_archive from item where item_id = %s" % (item_id))['in_archive']
    if is_archived=='t':
        item_date = dict_from_query("select text_value FROM metadatavalue WHERE item_id = %s and metadata_field_id = %s" % (item_id, get_field_id('dc.date.accessioned')))['text_value']
        archive_date = str(item_date)
    return archive_date

def query_for_doi (item_id):
    # Query database for the item's doi and return as string
    doi = dict_from_query("select text_value from metadatavalue where item_id = %s and metadata_field_id = %s" % (item_id, get_field_id('dc.identifier')))['text_value']
    return doi

def valid_date(s):
    format_ymd = "%Y-%m-%d"
    try:
        return datetime.strptime(s, format_ymd)
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main():
    parser = argparse.ArgumentParser(description='Start Date and End date.')
    parser.add_argument('-s', "--startdate", help="The Start Date - format YYYY-MM-DD ", required=True, type=valid_date)
    parser.add_argument('-e', "--enddate", help="The End Date - format YYYY-MM-DD ", required=True, type=valid_date)
 
    args = parser.parse_args()

    start_date = args.startdate
    end_date = args.enddate

    #Query shopping cart for items with payment dates between the start_date and end_date provided by user
    prov_field = get_field_id('dc.description.provenance')
    items = rows_from_query ("select cart_id, expiration, status, depositor, item, currency, country, voucher, total, transaction_id, journal, journal_sub, order_date, payment_date, notes from shoppingcart where payment_date BETWEEN '%s' AND '%s' and status='completed'" % (start_date, end_date))
    labels = dict(zip(items[0], range(0,len(items[0]))))

    # Open output file and print column labels to the file
    outFile = open('monthlyReport.csv', 'w')
    outFile.write('cart_id\texpiration\tstatus\tdepositor\titem\tDOI\tcurrency\tcountry\tvoucher\ttotal\ttransaction_id\tjournal\tjournal_sub\torder_date\tpayment_date\tNotes\tlast_mod_date\tarchive_date\n')
    print "cart_id\texpiration\tstatus\tdepositorvitem\tDOI\tcurrency\tcountry\tvoucher\ttotal\ttransaction_id\tjournal\tjournal_sub\torder_date\tpayment_date\tNotes\tlast_mod_date\tarchive_date"
    cnt = 0

    # Loop through items and for each item, assemble values into a string and print
    for item in items[1:-1]:
        # Query for values and combine all into a string and print to file
        next = build_output_string(item, labels)
        print '%s' % next
        outFile.write("%s\n" % next)
        cnt = cnt + 1

    outFile.close()
    print ("\n\n>>> Output for this report can be found in the file monthlyReport.csv located in the current directory")
    print (">>> Total number of shopping cart payments between '%s' and '%s': '%s'\n" % (start_date, end_date, cnt))

if __name__ == '__main__':
    main()
