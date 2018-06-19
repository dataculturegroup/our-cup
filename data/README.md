Getting Census Foreign-Born Population Data
===========================================

To download the Zip-Code Equivalence Table
------------------------------------------

1. Visit the Census 2010 [2010 ZIP Code Tabulation Area (ZCTA) Relationship Files Page](http://www.census.gov/geo/maps-data/data/zcta_rel_download.html)
2. Download the [2010 ZCTA to Census Tract Relationship File](http://www.census.gov/geo/maps-data/data/docs/rel/zcta_tract_rel_10.txt)


To dowload and update the ACS data
----------------------------------

1. Visit http://factfinder2.census.gov/
2. Click the Advanced Search option
3. Under Geographics, choose "Census Tract - 140", then pick a state and choose "All Census Tracts in [STATE]"
4. Repeat this for about half the states (you can't do all of them at once)
5. By the "Refine your search results:" field, search for topic B05006 and click go
6. Pick the most recent "ACS 5-year estimates" result and click it
7. Click download, pick data use, click ok, then click download again
8. Repeat from step 4 to select the other half of the states 
9. Open both "_with_ann" files and save them in utf8 encoding so we can import them correctly.
10. Edit `import_acs_data.py` to put in the path to both files
