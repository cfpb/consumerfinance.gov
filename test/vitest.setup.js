import { it, describe } from 'vitest';

// Make Jest-style xit and xdescribe available in Vitest.
globalThis.xit = it.skip;
globalThis.xdescribe = describe.skip;
