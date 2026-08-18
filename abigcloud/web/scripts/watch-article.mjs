#!/usr/bin/env node
/**
 * watch-article.mjs — republish a draft the moment it changes on disk.
 *
 * Pairs with `astro dev`. Brandon edits final.md (in mdlive, vim, whatever);
 * this notices the save, regenerates the site page from it, and Astro's dev
 * server hot-reloads the browser. Edit on one screen, watch the real site
 * update on the other.
 *
 * Run both together with:  npm run watch
 */
import { watch } from 'node:fs';
import { spawn } from 'node:child_process';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const WEB = resolve(HERE, '..');
const RESEARCH = resolve(WEB, '../..');
const DRAFT = join(RESEARCH, 'monologues', 'final.md');

let timer = null;
let running = false;

function publish(reason) {
	if (running) return;
	running = true;
	const t = new Date().toTimeString().slice(0, 8);
	process.stdout.write(`\n[${t}] ${reason} -> republishing\n`);
	const p = spawn(process.execPath, [join(HERE, 'build-article.mjs')], { stdio: 'inherit' });
	p.on('exit', (code) => {
		running = false;
		if (code !== 0) process.stdout.write(`  publish exited ${code}\n`);
	});
}

publish('startup');

// editors save by writing a temp file and renaming, so the watcher can fire
// several times per save; debounce so we publish once
watch(dirname(DRAFT), (_event, file) => {
	if (file !== 'final.md') return;
	clearTimeout(timer);
	timer = setTimeout(() => publish('final.md changed'), 250);
});

process.stdout.write(`watching ${DRAFT}\n`);
