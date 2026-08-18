#!/usr/bin/env node
/**
 * watch-content.mjs — re-resolve citations the moment a page changes.
 *
 * Pairs with `astro dev`. Brandon edits any page under content/ in mdlive;
 * this notices the save, resolves any new @/ citations and rebuilds the source
 * index, and Astro's dev server hot-reloads the browser. Edit on one screen,
 * watch the real site update on the other.
 *
 * Run both together with:  npm run watch
 */
import { watch } from 'node:fs';
import { spawn } from 'node:child_process';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const WEB = resolve(HERE, '..');
const RESEARCH = resolve(WEB, '..');
const CONTENT = join(WEB, 'content');

let timer = null;
let running = false;

function publish(reason) {
	if (running) return;
	running = true;
	const t = new Date().toTimeString().slice(0, 8);
	process.stdout.write(`\n[${t}] ${reason} -> republishing\n`);
	const p = spawn(process.execPath, [join(HERE, 'build-citations.mjs')], { stdio: 'inherit' });
	p.on('exit', (code) => {
		running = false;
		if (code !== 0) process.stdout.write(`  publish exited ${code}\n`);
	});
}

publish('startup');

// editors save by writing a temp file and renaming, so the watcher can fire
// several times per save; debounce so we publish once
watch(CONTENT, { recursive: true }, (_event, file) => {
	if (!file || !file.endsWith('.md')) return;
	clearTimeout(timer);
	timer = setTimeout(() => publish(`${file} changed`), 250);
});

process.stdout.write(`watching ${CONTENT}/**/*.md\n`);
