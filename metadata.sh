#!/bin/bash

cd hs-fulda/

results=metadata.json

#read metadata
iiifflat() {
	iiif-flat-metadata "$myjson" >> $results
}

for myjson in *.json; do
	echo "writing $myjson"
	iiifflat
done
