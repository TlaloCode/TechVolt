module.exports = {
    root: true,
    env: {
        browser: true,
        node: true,
    },

    parserOptions: {
        parser: '@babel/eslint-parser',
        requireConfigFile: false,
    },
    extends: ['@nuxtjs', 'plugin:nuxt/recommended', 'prettier'],
    plugins: ['prettier'],
    // add your custom rules here
    rules: {
        'vue/html-indent': ['error', 4],
        'vue/singleline-html-element-content-newline': 0,
        'vue/html-self-closing': 0,
        'vue/no-template-shadow': 'error',
        'vue/component-name-in-template-casing': ['error', 'PascalCase'],
        'vue/valid-v-slot': [
            'error',
            {
                allowModifiers: true,
            },
        ],
        'no-console': process.env.NODE_ENV === 'production' ? ['error', { allow: ['error'] }] : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
        'prettier/prettier': [
            'error',
            {
                endOfLine: 'lf',
            },
        ],
    },
    overrides: [
        {
            files: ['pages/**/*.vue', 'layouts/*.vue'],
            rules: {
                'vue/multi-word-component-names': 'off',
            },
        },
    ],
}
