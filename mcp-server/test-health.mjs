#!/usr/bin/env node

/**
 * Simple health check for the MCP server
 * This verifies the server starts and responds to requests
 */

import http from 'node:http';

const port = process.env.PORT || 3000;
const url = `http://localhost:${port}/mcp`;

console.log(`Testing MCP server at ${url}...`);

const options = {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/event-stream'
  }
};

const req = http.request(url, options, (res) => {
  console.log(`Status: ${res.statusCode}`);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    // Accept 200 (OK) and 400 (Bad Request) as successful responses.
    // 400 is considered a success here because the server may respond with 400 for invalid requests,
    // but this still proves the server is alive and processing requests.
    if (res.statusCode === 200 || res.statusCode === 400) {
      console.log('✓ Server is responding');
      process.exit(0);
    } else {
      console.log('✗ Unexpected status code');
      console.log(data);
      process.exit(1);
    }
  });
});

req.on('error', (error) => {
  console.error('✗ Server is not reachable:', error.message);
  process.exit(1);
});

req.write(JSON.stringify({
  jsonrpc: '2.0',
  method: 'initialize',
  id: 1,
  params: {}
}));
req.end();
