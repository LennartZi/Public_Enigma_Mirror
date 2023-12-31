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
let model = "I"

let plugboard = "#keyboard_plug"
let rotor_sub = '.rotor-substitutions'

describe('Variant Select', () => {
    it('Selects The Variant', () => {
      cy.visit(url)
      cy.setModel(model_selector, model)
      cy.wait(200)
    })
  })

  describe('Rotor Select', () => {
    it('Selects the Rotors', () => {
      cy.visit(url)
      cy.setModel(model_selector, model)
      cy.setRotors('I', 'V', 'II')

      cy.wait(200)
    })
  })

  describe('Keyboard Click', () => {
    it('Tests the Keyboard Highlight', () => {
        cy.visit(url)
        cy.setModel(model_selector, model)
        cy.setRotors('I', 'V', 'II')
        cy.setReflectors()

        cy.get(keys).contains("Q").click().then(() => {
            cy.get(keys).contains("Q").should('have.class', 'highlight')
        });
        cy.wait(200)
    })
  })

  describe('Lamppanel Click', () => {
    it('Tests the Lamppanel Highlight', () => {
        cy.visit(url)
        cy.setModel(model_selector, model)
        cy.setRotors('I', 'V', 'II')
        cy.setReflectors()

        cy.get(keys).contains("Q").click().then(() => {
            cy.get(lamps).contains("G").should('have.class', 'highlight-red')
          });
            cy.wait(200)
    })
  })

  
  
  describe('Keyboard Press', () => {
    it('Tests the Keyboard Highlight', () => {
        cy.visit(url)
        cy.setModel(model_selector, model)
        cy.setRotors('I', 'V', 'II')
        cy.setReflectors()
        
        cy.get('body').trigger('keydown', { keycode: 81, key: 'q', eventConstructor: 'KeyboardEvent' }) // q
        cy.wait(100)
        cy.get(keys).contains("Q").should('have.class', 'highlight')
        cy.get('body').trigger('keyup', { keycode: 81, key: 'q', eventConstructor: 'KeyboardEvent' })
        cy.wait(200)
    })
  })

  describe('Lamppanel Press', () => {
    it('Tests the Lamppanel Highlight', () => {
        cy.visit(url)
        cy.setModel(model_selector, model)
        cy.setRotors('I', 'V', 'II')
        cy.setReflectors()

        cy.get('body').trigger('keydown', { keycode: 81, key: 'q', eventConstructor: 'KeyboardEvent' }) // q
        cy.wait(100)
        cy.get(lamps).contains("G").should('have.class', 'highlight-red')
        cy.get('body').trigger('keyup', { keycode: 81, key: 'q', eventConstructor: 'KeyboardEvent' })
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
      cy.setModel(model_selector, model)
      cy.setRotors('I', 'V', 'II')
      cy.setReflectors()
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
        cy.setModel(model_selector, model)
        cy.setRotors('I', 'V', 'II')
        cy.setReflectors()

        //G zu Y Verbinden
        cy.get(plugboard).contains('G').click()
        cy.get(plugboard).contains('Y').click()

        //A zu Q Verbinden
        cy.get(plugboard).contains('A').click()
        cy.get(plugboard).contains('Q').click()

        //Q Klicken
        cy.get(keys).contains("A").click().then(()=>{

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
        cy.setModel(model_selector, model)
        cy.setRotors('I', 'V', 'II')

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

      cy.setCookie('variant', 'I')
      cy.setCookie('rotors', "[\"I\",\"V\",\"II\"]")
      cy.setCookie('plugboard', "{'T': 'G','G': 'T'}")
      cy.setCookie('positions', "[\"R\",\"J\", \"B\"]")
      cy.setCookie('reflector', 'UKW-C')
      cy.setCookie('input_history', 'HALLO')
      cy.setCookie('history', 'KBECV')
      cy.wait(200)

      //cy.reload()
      cy.wait(2500)

      cy.get('#resetDiv').click()
      
      cy.wait(200)
      cy.get(model_selector).invoke('text').then((text) => {
        expect(text).to.not.equal('I')
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

  //Encryption
describe('Full User Interaction', () => {
  it('Full User Interaction', () => {
    cy.visit(url)
    cy.setModel(model_selector, model)
    cy.setRotors('I', 'V', 'II')
    cy.setReflectors()

    cy.testUserInput(input_history,output_history, keys, usr_input)
    cy.checkHistory(input_history, output_history, usr_input)

    cy.get(output_history).invoke('text').then((text) => {
      encr_output = text
    });
  })
})

// Decryption
describe('User Interaction Decryption', () => {
  it('User Types the Encrypted '+usr_input, () => {
    cy.visit(url)
    cy.setModel(model_selector, model)
    cy.setRotors('I', 'V', 'II')
    cy.setReflectors()
    //Da ein neuer Buchstabe immer links in die History und nicht rechts vom alten geschrieben wird,
    //muss Encrypteter String reversed werden fuer den Input
    encr_output = encr_output.split('').reverse().join("")
    cy.testUserInput(input_history,output_history, keys, encr_output)

    cy.get(output_history).invoke('text').then((text) => {
    expect(text).to.equal(usr_input.split('').reverse().join(""))
    });
  })
})
