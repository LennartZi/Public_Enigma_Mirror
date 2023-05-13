describe('Visit Frontpage', () => {
  it('Visits the Enigma Frontpage', () => {
    cy.visit('http://localhost:8000/')
  })
})


describe('Test PUT', () => {
  it('Test Encrypt-API Call', () => {
    cy.request('PUT', 'http://localhost:8000/api/encrypt', { letter: 'Q' }).then(
  (response) => {
    // response.body is automatically serialized into JSON
    expect(response).property('status').to.equal(200)
    expect(response.body).to.have.length(1)
  }
)
  })
})

describe('Test Click', () => {
  it('Single User Interation', () => {
    cy.visit('http://localhost:8000/')
    //  clicks Q, tests if highlighted, then if highlight gone, then if output field has 1 letter
    cy.contains('Q').click()
    cy.contains('Q').should('have.class', 'highlight')
    cy.contains('Q').not('have.class', 'highlight')
    
    cy.get(".output").invoke('text').then((text) => {
      expect(text).to.have.length(1)
  });


  })
})

describe('Test Keyboard Input', () => {
  it('Single User Interation', () => {
    cy.visit('http://localhost:8000/')
    cy.get('body').type('{q}');
    cy.get(".output").invoke('text').then((text) => {
      expect(text).to.have.length(1)
  });
  })
})



describe('Full User Input', () => {
  it('User Types the Word HELLO', () => {
    cy.visit('http://localhost:8000/')
    let inp = "HELLO"
    for (let i = 0; i < inp.length; i++) {
      cy.contains(inp[i]).click()
      cy.contains(inp[i]).should('have.class', 'highlight')
      
    }

    for (let i = 0; i < inp.length; i++) {
      cy.contains(inp[i]).not('have.class', 'highlight')
    }

    cy.get(".output").invoke('text').then((text) => {
      expect(text).to.have.length(inp.length)
  });
  })
})



//Same as User Input but with every Letter
describe('Test Every Letter', () => {
  it('Click Every Letter for Function Test', () => {
    cy.visit('http://localhost:8000/')
    let inp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for (let i = 0; i < inp.length; i++) {
      cy.contains(inp[i]).click()
      cy.contains(inp[i]).should('have.class', 'highlight')
    }

    for (let i = 0; i < inp.length; i++) {
      cy.contains(inp[i]).not('have.class', 'highlight')
    }

    cy.get(".output").invoke('text').then((text) => {
      expect(text).to.have.length(inp.length)
  });
  })
})