#! /bin/bash
set -e

FILTER_COMMAND=filterShoppingCart.pl
PREVIOUS_ID_FILE=shoppingCartIdsSeenInReports.txt

echo Starting monthly report. NOTE: This command must be run from the directory that contains the script. Make sure this directory has been updated from the master branch. Output will go to /tmp

echo Export archived
psql -U dryad_app -d dryad_repo -c "\copy (select * from shoppingcart, item, metadatavalue where shoppingcart.status='completed' and shoppingcart.item=metadatavalue.item_id and shoppingcart.item=item.item_id and item.in_archive=TRUE and metadatavalue.metadata_field_id=11) to '/tmp/shoppingArchived.csv' with CSV;"

echo Export blackout
psql -U dryad_app -d dryad_repo -c "\copy (select * from shoppingcart, item where shoppingcart.status='completed' and shoppingcart.item=item.item_id and item.item_id in (select item_id from metadatavalue where text_value like '%Entered publication blackout%' and item_id not in (select item_id  from metadatavalue where text_value like '%Approved for entry into archive%')))  to '/tmp/shoppingBlackout.csv' with CSV;"

echo Export fake blackout
psql -U dryad_app -d dryad_repo -c "\copy (select * from shoppingcart, item where shoppingcart.item=item.item_id and item.item_id in (select item_id from workflowitem where workflow_id in (select workflow_item_id from taskowner where owner_id = 949))) to '/tmp/shoppingFakeBlackout.csv' with CSV;"

echo Combine all charged transactions
cat /tmp/shoppingArchived.csv /tmp/shoppingBlackout.csv > /tmp/shoppingCharged.csv

echo Filtering previously-reported transactions
$FILTER_COMMAND $PREVIOUS_ID_FILE /tmp/shoppingCharged.csv >/tmp/shoppingChargedFiltered.csv 

# For the list of IDs to work properly, we need to restrict the report to the correct date range (i.e., Postgres queries need to be bounded by an end date)


#echo Tracking newly-reported IDs
#sed 's/,.*//' /tmp/shoppingChargedFiltered.csv >> $PREVIOUS_ID_FILE
#cat $PREVIOUS_ID_FILE | sort -g  >/tmp/monthlyReportTempFile.txt
#rm $PREVIOUS_ID_FILE
#mv /tmp/monthlyReportTempFile.txt $PREVIOUS_ID_FILE

#echo Committing newly-reported IDs
#git add $PREVIOUS_ID_FILE
#git commit -m "Monthly update of previously-reported IDs"

echo 
echo "TO FINISH REPORT (still needs to be automated) see http://wiki.datadryad.org/Monthly_Reports. Next step is #3."
