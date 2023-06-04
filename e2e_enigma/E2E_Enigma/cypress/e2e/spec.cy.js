//Testing Variables
let output_history = "#outputHistory"
let input_history = "#inputHistory"
let keys = ".key_input"
let model_selector = "#variantSelect"
let model = "I"
//Encrypt - Decrypt Test
let usr_input = "HELLO"
let encr_output = ""
// Url
let main_service = Cypress.env('MAIN_SERVICE')
let url = 'http://' + main_service
let api_encrypt = url + '/api/encrypt'


// Test Frontpage Loading
describe('Visit Frontpage', () => {
  it('Visits the Enigma Frontpage', () => {
    cy.visit(url)
  })
})

// Api Call Test
describe('Test PUT', () => {
  it('Test Encrypt-API Call', () => {
    cy.request('PUT', api_encrypt, { letter: 'Q' }).then(
  (response) => {
    // response.body is automatically serialized into JSON
    expect(response).property('status').to.equal(200)
    expect(response.body).to.have.length(1)
  }
)
  })
})

// Test Keyboard Input
describe('Test Keyboard Input', () => {
  it('Single User Interation', () => {
    cy.setupTest(url, model_selector, model)
    cy.get('body').type('{q}');
    cy.wait(65)
    cy.get(output_history).invoke('text').then((text) => {
      expect(text).to.have.length(1)
  });
  })
})

// Same as User Input but with every Letter
describe('Test Every Letter', () => {
  it('Click Every Letter for Function Test', () => {
    cy.setupTest(url, model_selector, model)

    let inp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cy.testUserInput(input_history, output_history, keys, inp)
    cy.checkHistory(input_history, output_history, inp)
  })
})

//Encryption
describe('Full User Interaction', () => {
  it('Full User Interaction', () => {
    cy.setupTest(url, model_selector, model)

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
    cy.setupTest(url, model_selector, model)
    //Da ein neuer Buchstabe immer links in die History und nicht rechts vom alten geschrieben wird,
    //muss Encrypteter String reversed werden fuer den Input
    encr_output = encr_output.split('').reverse().join("")
    cy.testUserInput(input_history,output_history, keys, encr_output)

    cy.get(output_history).invoke('text').then((text) => {
    expect(text).to.equal(usr_input.split('').reverse().join(""))
    });
  })
})

