import * as fs from 'fs';
import fancyLog from 'fancy-log';
import workboxBuild from 'workbox-build';
import environment from '../../../../config/environment.js';
const { processed, unprocessed } = environment.paths;
import path from 'path';

// Constants
const APP_NAME = 'regulations3k';
// This'll need to be changed if the app doesn't live at cf.gov/regulations
const APP_PATH = 'policy-compliance/rulemaking/regulations';
const SERVICE_WORKER_FILENAME = `${APP_NAME}-service-worker.js`;
const SERVICE_WORKER_DEST = `cfgov/${APP_NAME}/jinja2/${APP_NAME}/${SERVICE_WORKER_FILENAME}`;
const MANIFEST_FILENAME = `${APP_NAME}-manifest.json`;
const MANIFEST_SRC = `${unprocessed}/apps/${APP_NAME}/${MANIFEST_FILENAME}`;
const MANIFEST_DEST = `${processed}/apps/${APP_NAME}/${MANIFEST_FILENAME}`;

const SERVICE_WORKER_CONFIG = {
  swDest: SERVICE_WORKER_DEST,
  globDirectory: processed,
  globPatterns: [
    `apps/${APP_NAME}/css/main.css`,
    `apps/${APP_NAME}/js/index.js`,
  ],
  modifyURLPrefix: {
    'apps/': '/static/apps/',
  },
  runtimeCaching: [
    {
      urlPattern: new RegExp(`/${APP_PATH}/`),
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: `${APP_NAME}-content`,
        expiration: {
          maxAgeSeconds: 60 * 60 * 3,
        },
      },
    },
    {
      urlPattern: new RegExp(`/static/apps/${APP_NAME}`),
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: `${APP_NAME}-assets`,
        expiration: {
          maxAgeSeconds: 60 * 60 * 3,
        },
      },
    },
    {
      urlPattern: new RegExp('/static/(css|js|fonts|img)'),
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: 'cfpb-assets',
        expiration: {
          maxAgeSeconds: 60 * 60 * 3,
        },
      },
    },
  ],
  sourcemap: false,
  inlineWorkboxRuntime: true,
};

const ensureDirectoryExistence = (filePath) => {
  const dirname = path.dirname(filePath);
  if (fs.existsSync(dirname)) {
    return true;
  }
  ensureDirectoryExistence(dirname);
  return fs.mkdirSync(dirname);
};

/**
 * Run a service worker to copy a manifest file.
 */
function runWorkerAndManifest() {
  fancyLog('Started generating service worker file...');
  ensureDirectoryExistence(SERVICE_WORKER_DEST);
  workboxBuild
    .generateSW(SERVICE_WORKER_CONFIG)
    .then(({ count, size }) => {
      fancyLog(
        `Generated ${SERVICE_WORKER_DEST}, which will precache ${count} files, totaling ${size} bytes.`,
      );
    })
    .catch((err) => {
      fancyLog(`Error generating service worker file: ${err}`);
    });

  fancyLog("Copying eRegs' manifest...");
  ensureDirectoryExistence(MANIFEST_DEST);
  fs.copyFile(MANIFEST_SRC, MANIFEST_DEST, (err) => {
    if (err) {
      return fancyLog(`Error copying eRegs' manifest: ${err}`);
    }
    return fancyLog(`Successfully copied eRegs' manifest to ${MANIFEST_DEST}`);
  });
}

export { runWorkerAndManifest };
