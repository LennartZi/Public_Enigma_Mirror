const { defineConfig } = require("cypress");

module.exports = defineConfig({
  viewportHeight: 860,
  env: {
    MAIN_SERVICE: 'localhost:8000',
  },
  e2e: {
    specPattern: "cypress/e2e/*.cy.{js,jsx,ts,tsx}",
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
  "retries": {
    "runMode": 2,
    "openMode": 0,
  },
});
