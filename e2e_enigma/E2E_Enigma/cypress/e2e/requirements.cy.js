//Testing Variables
let output_history = "#outputHistory"
let input_history = "#inputHistory"
let keys = ".key_input"
let lamps = "#keyboard_output"
//Encrypt - Decrypt Test
let usr_input = "HELLO"
let encr_output = ""
// Url
let main_service = Cypress.env('MAIN_SERVICE')
let url = 'http://' + main_service
let api_encrypt = url + '/api/encrypt'

let model_selector = "#variantSelect"
let model = ["M3", "I", "D"]


describe('Variant Select', () => {
    it('Selects The Variant', () => {
      cy.visit(url)


      for (let i = 0; i < model.length; i++){
      cy.setModel(model_selector, model[i])
      }
    })
  })

  describe('Rotor Select', () => {
    it('Selects the Rotors', () => {
      cy.visit(url)
      cy.setModel(model_selector, model[1])
      cy.setRotors()
    })
  })

  describe('Keyboard Click', () => {
    it('Tests the Keyboard Highlight', () => {
        cy.visit(url)
        cy.setModel(model_selector, model[1])
        cy.setRotors()

        cy.get(keys).contains("Q").click().then(() => {
            cy.get(keys).contains("Q").should('have.class', 'highlight')
        });
        
    })
  })

  describe('Lamppanel Click', () => {
    it('Tests the Lamppanel Highlight', () => {
        cy.visit(url)
        cy.setModel(model_selector, model[1])
        cy.setRotors()

        cy.get(keys).contains("Q").click().then(() => {
            cy.get(lamps).contains("U").should('have.class', 'highlight-red')});
        
    })
  })

  describe('Keyboard Press', () => {
    it('Tests the Keyboard Highlight', () => {
        cy.visit(url)
        cy.setModel(model_selector, model[1])
        cy.setRotors()
        
        cy.get('body').type('{Q}').then(() => {
            cy.get(keys).contains("Q").should('have.class', 'highlight')
        });
    })
  })

  describe('Lamppanel Press', () => {
    it('Tests the Lamppanel Highlight', () => {
        cy.visit(url)
        cy.setModel(model_selector, model[1])
        cy.setRotors()

        cy.get('body').type('{Q}').then(() => {
            cy.get(lamps).contains("U").should('have.class', 'highlight-red')
        });
        
    })
  })


  describe('Cookies', () => {
    it('Cookies', () => {
      
      cy.visit(url)
      cy.setCookie('variant', 'I')
      cy.setCookie('input_history', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
      cy.setCookie('history', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
      
      cy.reload()
      cy.setModel(model_selector, model[1])
      cy.setRotors()
      cy.get(keys).contains("Q").click().then(() => {
        cy.get(lamps).contains("U").should('have.class', 'highlight-red')});

        cy.get(keys).contains("P").click()
    })
    
  })