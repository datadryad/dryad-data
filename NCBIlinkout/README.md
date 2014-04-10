Data NCBI LinkOut connections to Dryad
--------------------------------------

### Files or directories:
- `access-stats/`: Access statistics for [NCBI LinkOut connections to
  Dryad](http://wiki.datadryad.org/NCBI_LinkOut). NCBI collects these, and
  sends them to Dryad on a monthly basis.

### Other information:

* According to NCBI's notification to LinkOut providers, _"[due] to a
  technical problem, we lost some of the hits count from 2014-03-14 to
  2014-03-28.  Thus, your statistics for March 2014 will be lower than
  normal.  We apologize to any inconvenience."_

* The commit messages for the 2013 reports (i.e., all prior to
  `7893-2014-01-10.csv`) are off by one month. For example, commit
  be20bdb6e3e7520a7cf37dbeb6cc9c695bd4c443 states to be a report for
  November 2013, but the stats are in fact for October 2013. As a
  consequence, there are two commits stating to be the report for
  December 2013: one that in reality is for November 2013
  (ba4fdb2414b388177ee3dcfd5c8d5dfaa9934fb1), and one that indeed is
  for December 2013 (d3573ff949f30964d80adf5b4e45e13351aa5354).
