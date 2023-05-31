//Testing Variables
let output_history = "#outputHistory"
let input_history = "#inputHistory"
let keys = ".key_input"
//Encrypt - Decrypt Test
let usr_input = "HELLO"
let encr_output = ""
// Url
let main_service = Cypress.env('MAIN_SERVICE')
let url = 'http://' + main_service
let api_encrypt = url + '/api/encrypt'

// Custom Command To Test Input And Backend Respond
Cypress.Commands.add('testUserInput', (inp) => {
  for (let i = 0; i < inp.length; i++) {
    cy.get(keys).contains(inp[i]).click()
    cy.get(keys).contains(inp[i]).should('have.class', 'highlight')
    cy.wait(65)
  }

  for (let i = 0; i < inp.length; i++) {
    cy.get(keys).contains(inp[i]).not('have.class', 'highlight')
  }

  cy.get(output_history).invoke('text').then((text) => {
    expect(text).to.have.length(inp.length)
});
})

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

// Test Single Click
describe('Test Click', () => {
  it('Single User Interation', () => {
    cy.visit(url)
    //  clicks Q, tests if highlighted, then if highlight gone, then if output field has 1 letter
    cy.get(keys).contains('Q').click()
    cy.get(keys).contains('Q').should('have.class', 'highlight')
    cy.get(keys).contains('Q').not('have.class', 'highlight')
    
    cy.wait(65)
    cy.get(output_history).invoke('text').then((text) => {
      expect(text).to.have.length(1)
  });


  })
})

// Test Keyboard Input
describe('Test Keyboard Input', () => {
  it('Single User Interation', () => {
    cy.visit(url)
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
    cy.visit(url)
    let inp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cy.testUserInput(inp)
  })
})


// Normal User Interaction
describe('User Interaction Encryption', () => {
  it('User Types the Word '+usr_input, () => {
    cy.visit(url)
    cy.testUserInput(usr_input)

    cy.get(output_history).invoke('text').then((text) => {
      encr_output = text
    });
  })
})

// Decryption
describe('User Interaction Decryption', () => {
  it('User Types the Encrypted '+usr_input, () => {
    cy.visit(url)
    //Da ein neuer Buchstabe immer links in die History und nicht rechts vom alten geschrieben wird,
    //muss Encrypteter String reversed werden fuer den Input
    encr_output = encr_output.split('').reverse().join("")
    cy.testUserInput(encr_output)

    cy.get(output_history).invoke('text').then((text) => {
    expect(text).to.equal(usr_input.split('').reverse().join(""))
    });
  })
})

