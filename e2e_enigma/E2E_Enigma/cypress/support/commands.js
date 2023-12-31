Cypress.Commands.add('testUserInput', (input_history, output_history, keys, inp) => {
    for (let i = 0; i < inp.length; i++) {
      cy.get(keys).contains(inp[i]).click()
      cy.get(keys).contains(inp[i]).should('have.class', 'highlight')
      cy.wait(65)
    }
  
    for (let i = 0; i < inp.length; i++) {
      cy.get(keys).contains(inp[i]).not('have.class', 'highlight')
    }
    
})
  
Cypress.Commands.add('checkHistory', (input_history, output_history, inp) => {
    //Output Test
    cy.get(output_history).invoke('text').then((text) => {
        expect(text).to.have.length(inp.length)
      });
    //Input History Test
    cy.get(input_history).invoke('text').then((text) => {
        expect(text).to.equal(inp.split('').reverse().join(""))
      });  

})

Cypress.Commands.add('setModel', (element, inp) => {
    cy.get(element).select(inp)
})

Cypress.Commands.add('setRotors', (first, second, last) => {
    //cy.get("#rotor1").click()
    cy.get('ol#rotorSelection li:first').click()
    cy.get('ol#rotorSelection li:last').click()
    cy.get('ol#rotorSelection li:first').next().click()

    //cy.get('ol#selectedRotor li:first').should("have.value", "I")
    cy.get('ol#selectedRotor .rotor-container:first span').invoke('text').then((text) => {
        expect(text).to.equal(first)
      });
    cy.wait(200)
    cy.get('ol#selectedRotor .rotor-container:last span').invoke('text').then((text) => {
        expect(text).to.equal(last)
      });
    cy.wait(200)
    cy.get('ol#selectedRotor .rotor-container:first').next().find('span').invoke('text').then((text) => {
        expect(text).to.equal(second)
      });
    cy.wait(200)
})

Cypress.Commands.add('setRotorsCustom', () => {
  //cy.get("#rotor1").click()
  cy.get('ol#rotorSelection li:first').click()
  cy.get('ol#rotorSelection li:last').click()
  cy.get('ol#rotorSelection li:first').next().click()

  //cy.get('ol#selectedRotor li:first').should("have.value", "I")
  cy.get('ol#selectedRotor .rotor-container:first span').invoke('text').then((text) => {
      expect(text).to.equal('I')
    });
  cy.wait(200)
  cy.get('ol#selectedRotor .rotor-container:last span').invoke('text').then((text) => {
      expect(text).to.equal("II")
    });
  cy.wait(200)
  cy.get('ol#selectedRotor .rotor-container:first').next().find('span').invoke('text').then((text) => {
      expect(text).to.equal("III")
    });
  cy.wait(200)
})

Cypress.Commands.add('setReflectors', (rotor_name = 'UKW-A') => {
    cy.get('ol#reflectorSelection li:first').click()
    cy.get('li[data-value="reflector1"].selected').invoke('text').then((text) => {
        expect(text).to.equal(rotor_name)
      });
})

Cypress.Commands.add('setupTest', (url, model_selector,model) => {
    cy.visit(url)
    cy.setModel(model_selector, model)
    cy.wait(65)
    cy.setRotors()
    cy.wait(100)
    cy.setReflectors()
    cy.wait(65)
})
