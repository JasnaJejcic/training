#!/bin/sh

rm build/func.zip
cd build
cp ../src/index.js .
zip func.zip index.js
rm index.js

cp -r ../src/node_modules .
zip -r func.zip node_modules
rm -rf node_modules
cd ..