// Custom Command To Test Input And Backend Respond
Cypress.Commands.add('testUserInput', (inp) => {
  for (let i = 0; i < inp.length; i++) {
    cy.contains(inp[i]).click()
    cy.contains(inp[i]).should('have.class', 'highlight')
    cy.wait(100)
  }

  for (let i = 0; i < inp.length; i++) {
    cy.contains(inp[i]).not('have.class', 'highlight')
  }

  cy.get(".output").invoke('text').then((text) => {
    expect(text).to.have.length(inp.length)
});
})

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

// Test Single Click
describe('Test Click', () => {
  it('Single User Interation', () => {
    cy.visit(url)
    //  clicks Q, tests if highlighted, then if highlight gone, then if output field has 1 letter
    cy.contains('Q').click()
    cy.contains('Q').should('have.class', 'highlight')
    cy.contains('Q').not('have.class', 'highlight')
    
    cy.wait(100)
    cy.get(".output").invoke('text').then((text) => {
      expect(text).to.have.length(1)
  });


  })
})

// Test Keyboard Input
describe('Test Keyboard Input', () => {
  it('Single User Interation', () => {
    cy.visit(url)
    cy.get('body').type('{q}');
    cy.wait(100)
    cy.get(".output").invoke('text').then((text) => {
      expect(text).to.have.length(1)
  });
  })
})

// Normal User Interaction
describe('User Interaction', () => {
  it('User Types the Word HELLO', () => {
    cy.visit(url)
    let inp = "HELLO"
    cy.testUserInput(inp)
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
