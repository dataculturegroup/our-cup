import eslintPluginSvelte from 'eslint-plugin-svelte';
import * as svelteParser from 'svelte-eslint-parser';
import * as espree from "espree";
import svelteConfig from './svelte.config.js';

export default [
  ...eslintPluginSvelte.configs.recommended,
  {
    files: ['**/*.svelte'],
    languageOptions: {
      parser: svelteParser,
      parserOptions: {
        parser: {
          js: espree,
        },
        extraFileExtensions: ['.svelte'],
        svelteConfig
      }
    }
  }
];