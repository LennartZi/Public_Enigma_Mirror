const { defineConfig } = require("cypress");

module.exports = defineConfig({
  viewportHeight: 860,
  env: {
    MAIN_SERVICE: 'localhost:8000',
  },
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
