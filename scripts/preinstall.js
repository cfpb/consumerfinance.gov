if (process.env.npm_execpath.indexOf('yarn') === -1) {
  console.error('\x1b[41m', 'You must use Yarn to install dependencies:');
  console.error('\x1b[41m', '  $ yarn install');
  console.error('\x1b[40m');
  process.exit(1);
}
