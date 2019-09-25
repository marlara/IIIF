#!/bin/bash

# trap for exiting while in subshell
set -E
trap '[ "$?" -ne 77 ] || exit 77' ERR

results=metadata.json

#read metadata
iiifflat() {
	iiif-flat-metadata "$myjson" >> $results
}

( # start subshell
if cd ./hs-fulda ; then
	: # change directory successful, continue...
else
	exit 77
fi
for myjson in *.json; do
	echo "writing $myjson"
	iiifflat	
done
) # end subshell

