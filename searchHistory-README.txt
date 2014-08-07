A log of searches performed in Dryad is now available at:
http://datadryad.org/downloads/dryadSearchLogs.txt

The search logs are not presented here directly, due to GitHub's limit on file size.

The search logs were extracted from our main Apache access logs using the following command:
zgrep "] \"GET /discover?query=" /opt/dryad-data/log_archives/var/log/httpd/dryad/datadryad.org-access_log*.gz | grep -v 192.107.175.11| awk '{ print $4 " " $7 } ' | grep -v "/discover?query=&submit=Go" | sed -e 's/&submit=Go//' | sed -e 's/\/discover?//' | sed -e 's/\[//' >dryadSearchLogs.txt

The extraction command excludes lines from the logs that do not contain searches. It also excludes searches from one particular IP address. This IP constantly queries Dryad for random dictionary words, and is not considered an informative addition to the logs. 

The extraction command filters the appropriate lines to remove identifiable information such as IP addresses and user agents. The resultant file contains timestamps and query strings, separated by a space.
