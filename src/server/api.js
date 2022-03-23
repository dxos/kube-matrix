//
// Copyright 2021 DXOS.org
//

const { spawnSync } = require('child_process');

const scriptMap = {
  'default': './scripts/run_test.py',
  'boot': './scripts/run_boot.py',
  'reset': './scripts/run_reset.py',
  'bitmap': './scripts/run_bitmap.py',
  'demo': './scripts/run_demo.py',
  'test': './scripts/run_test.py',
  'life': './scripts/run_life.py'
}

// TODO(burdon): Logging.
const apiService = async ({ action, bitmap }) => {
  if (action === 'noop') {
    return {
      status: 0,
      action
    };
  }

  const script = scriptMap[action] ?? scriptMap['default'];
  console.log(`Running script: ${script}`);

  try {
    const { status, stderr } = spawnSync('python3', [script], { encoding: 'utf8' });
    let error;
    if (status !== 0) {
      error = stderr;
      console.error('ERROR', stderr);
    }

    return {
      status,
      action,
      script,
      error
    };
  } catch (err) {
    console.error('ERROR', err);
    return err;
  }
};

module.exports = apiService;
