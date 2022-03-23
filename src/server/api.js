//
// Copyright 2021 DXOS.org
//

const { spawnSync } = require('child_process');

const scriptMap = {
  'default': './scripts/boot_anim.py',
  'test': './scripts/led_demo.py',
  'life': './scripts/game_of_life.py'
}

// TODO(burdon): Logging.
const apiService = async ({ action }) => {
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
