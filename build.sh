#!/bin/sh
fn='anki-add'
zip "${fn}.zip" *.py
[ -d "build" ] || mkdir "build"
echo '#!/bin/env python3' | cat - "${fn}.zip" > "build/$fn"
rm "$fn.zip"
chmod +x "build/$fn"