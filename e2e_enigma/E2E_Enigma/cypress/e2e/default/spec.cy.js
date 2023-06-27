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


