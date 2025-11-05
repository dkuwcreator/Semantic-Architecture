#!/bin/sh
# Post-build script to add shebang to the compiled server file
sed -i '1i#!/usr/bin/env node' dist/server.js 2>/dev/null || sed -i '' '1i\
#!/usr/bin/env node
' dist/server.js
chmod +x dist/server.js
