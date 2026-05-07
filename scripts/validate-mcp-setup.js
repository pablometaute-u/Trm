#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function parseEnvFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const result = {};

  for (const line of content.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const equalIndex = trimmed.indexOf('=');
    if (equalIndex <= 0) continue;

    const key = trimmed.slice(0, equalIndex).trim();
    const value = trimmed.slice(equalIndex + 1).trim();
    result[key] = value;
  }

  return result;
}

function isPresent(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function isValidPort(value) {
  const n = Number(value);
  return Number.isInteger(n) && n > 0 && n <= 65535;
}

function readArg(flagName) {
  const idx = process.argv.indexOf(flagName);
  if (idx === -1) return null;
  return process.argv[idx + 1] || null;
}

function main() {
  const envArg = readArg('--env');
  const envFile = envArg
    ? path.resolve(envArg)
    : path.resolve(process.cwd(), '.env');

  if (!fs.existsSync(envFile)) {
    console.error(`❌ Env file not found: ${envFile}`);
    process.exit(1);
  }

  const env = parseEnvFile(envFile);
  const requiredAbap = [
    'SAP_HOST',
    'SAP_PORT',
    'SAP_CLIENT',
    'SAP_USER',
    'SAP_PASSWORD',
    'SAP_ROUTER'
  ];

  const missingAbap = requiredAbap.filter((key) => !isPresent(env[key]));
  if (missingAbap.length > 0) {
    console.error(`❌ Missing ABAP MCP variables: ${missingAbap.join(', ')}`);
    process.exit(1);
  }

  if (!isValidPort(env.SAP_PORT)) {
    console.error(`❌ Invalid SAP_PORT: ${env.SAP_PORT}`);
    process.exit(1);
  }

  const missingNotes = ['SAP_NOTES_USERNAME', 'SAP_NOTES_PASSWORD']
    .filter((key) => !isPresent(env[key]));

  const major = Number(process.versions.node.split('.')[0]);
  if (!Number.isInteger(major) || major < 18) {
    console.error(`❌ Node.js 18+ required. Current: ${process.versions.node}`);
    process.exit(1);
  }

  console.log('✅ Node.js version OK:', process.versions.node);
  console.log('✅ ABAP ADT MCP required variables OK');

  if (missingNotes.length > 0) {
    console.warn(`⚠️ SAP Notes MCP variables missing: ${missingNotes.join(', ')}`);
    console.warn('   You can continue with ABAP ADT MCP, but @sap-notes will not work.');
  } else {
    console.log('✅ SAP Notes MCP required variables OK');
  }

  console.log('✅ MCP setup validation completed successfully');
}

main();
