module.exports = {
    env: {
      browser: true,
      es2021: true,
    },
    extends: [
      'eslint:recommended',
      'plugin:svelte/recommended', // Use the recommended Svelte rules
      'plugin:prettier/recommended'
    ],
    overrides: [
      {
        files: ['*.svelte'], // Apply these rules only to Svelte files
        processor: 'svelte/svelte',
      },
    ],
    parserOptions: {
      ecmaVersion: 2021,
      sourceType: 'module',
    },
    plugins: ['svelte'],
    rules: {
      // Add custom rules or override default ones here
    },
  };