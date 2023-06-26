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
let api_positions = url + '/api/rotor/0/position'

let model_selector = "#variantSelect"
let model = ["M3", "I", "B (A-133 modified)"]

let plugboard = "#keyboard_plug"
let rotor_sub = '.rotor-substitutions'

describe('Variant Select', () => {
    it('Selects The Variant', () => {
      cy.visit(url)


      for (let i = 0; i < model.length; i++){
      cy.setModel(model_selector, model[i])
      }

      cy.wait(200)
    })
  })

  describe('Rotor Select', () => {
    it('Selects the Rotors', () => {
      cy.visit(url)
      cy.setModel(model_selector, model[1])
      cy.setRotors()

      cy.wait(200)
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
        cy.wait(200)
    })
  })

  describe('Lamppanel Click', () => {
    it('Tests the Lamppanel Highlight', () => {
        cy.visit(url)
        cy.setModel(model_selector, model[1])
        cy.setRotors()

        cy.get(keys).contains("Q").click().then(() => {
            cy.get(lamps).contains("U").should('have.class', 'highlight-red')
          });
            cy.wait(200)
    })
  })

  //Broken Test
  /*
  describe('Keyboard Press', () => {
    it('Tests the Keyboard Highlight', () => {
        cy.visit(url)
        cy.setModel(model_selector, model[1])
        cy.setRotors()
        
        cy.get('body').type('{Q}').then(() => {
            cy.get(keys).contains("Q").should('have.class', 'highlight')
        });
    })
  })*/

  describe('Lamppanel Press', () => {
    it('Tests the Lamppanel Highlight', () => {
        cy.visit(url)
        cy.setModel(model_selector, model[1])
        cy.setRotors()

        cy.get('body').trigger('keydown', { keycode: 81 }) // q
        cy.wait(100)
        cy.get(lamps).contains("U").should('have.class', 'highlight-red')
        cy.get('body').trigger('keyup', { keycode: 81 })
        cy.wait(200)
    })
  })


  describe('Cookies', () => {
    it('Cookies', () => {
      
      cy.visit(url)
      cy.setCookie('variant', 'I')
      cy.setCookie('input_history', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
      cy.setCookie('history', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
      cy.wait(200)
      cy.reload()
      cy.wait(200)
      cy.setModel(model_selector, model[1])
      cy.setRotors()
      cy.get(keys).contains("Q").click()
        cy.wait(200)
        cy.get(keys).contains("P").click()
        cy.wait(200)
        cy.get(input_history).invoke('text').then((text) => {
          expect(text).to.equal('PQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        }); 
        cy.wait(200)
    })
  })



  describe('Plugboard', () => {
    it('Tests the Plugboard', () => {

        //Mit dieser Konfiguration kommt beim Q klicken am Beginn U Raus
        cy.visit(url)
        cy.setModel(model_selector, model[1])
        cy.setRotors()

        //U zu Y Verbinden
        cy.get(plugboard).contains('U').click()
        cy.get(plugboard).contains('Y').click()

        //Q Klicken
        cy.get(keys).contains("Q").click().then(()=>{

          cy.wait(200)
          //Checken ob Output statt U jetzt Y rauskommt wegen Plugboard setting
          cy.get(output_history).invoke('text').then((text) => {
          expect(text).to.equal('Y')
        }); 
        });

        cy.wait(200)

    })
  })

  describe('Ring Settings', () => {
    it('Tests the Rotor Substitution and Reflector', () => {
        cy.visit(url)
        cy.setModel(model_selector, model[1])
        cy.setRotors()

        //cy.get(rotor_sub).contains('E').select('O')
        cy.get('ol#selectedRotor .rotor-substitutions:first').select("K")
        //cy.wait(200)
        //cy.get('ol#selectedRotor .rotor-substitutions:first').eq(1).select("Z")
        cy.wait(200)
        cy.get('ol#selectedRotor .rotor-substitutions:last').select("D")

        cy.wait(200)
        //Wählt ersten Reflektor
        cy.get('#reflectorSelection li').first().click()
        cy.wait(200)
        //Klickt Letzten Reflektor
        cy.get('#reflectorSelection li').last().click()
        cy.wait(200)
        //Nur einer sollte Gleichzeitig gewählt sein darum Test
        cy.get('#reflectorSelection li').first().should('have.class', 'selected')
        cy.wait(200)
        cy.get('#reflectorSelection li').first().not('have.class', 'selected')

        cy.wait(200)
    })
  })


  describe('Retain State', () => {
    it('Tests if State is loaded with Cookies', () => {
      cy.visit(url)

      cy.setCookie('variant', 'M3')
      cy.setCookie('rotors', "[\"I\",\"VII\",\"IV\"]")
      cy.setCookie('plugboard', "{'E': 'F','F': 'E'}")
      cy.setCookie('positions', "[\"A\",\"S\", \"I\"]")
      cy.setCookie('reflector', 'UKW-B')
      cy.setCookie('input_history', 'HALLO')
      cy.setCookie('history', 'QVZDM')
      cy.wait(200)

      //cy.reload()
      cy.wait(2500)

      cy.get('#resetDiv').click()
      
      cy.wait(200)
      cy.get(model_selector).invoke('text').then((text) => {
        expect(text).to.not.equal('M3')
      });
      cy.wait(200)
      cy.get('ol#selectedRotor .rotor-container:first span').invoke('text').then((text) => {
        expect(text).to.equal('X')
      });
    cy.wait(200)
    cy.get('ol#selectedRotor .rotor-container:last span').invoke('text').then((text) => {
        expect(text).to.equal("X")
      });
    cy.wait(200)
    cy.get('ol#selectedRotor .rotor-container:first').next().find('span').invoke('text').then((text) => {
        expect(text).to.equal("X")
      });
    cy.wait(200)

    cy.get(output_history).invoke('text').then((text) => {
      expect(text).to.have.length(0)
    });

    cy.wait(200)
  
  cy.get(input_history).invoke('text').then((text) => {
    expect(text).to.have.length(0)
    });  

    })
  })
