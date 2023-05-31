const { defineConfig } = require("cypress");

module.exports = defineConfig({
  env: {
    MAIN_SERVICE: 'localhost:8000',
  },
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
