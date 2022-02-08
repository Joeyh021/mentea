// main.spec.js created with Cypress
//
// Start writing your Cypress tests below!
// If you're unfamiliar with how Cypress works,
// check out the link below and learn how to write your first test:
// https://on.cypress.io/writing-first-test

describe('Main app functionality', () => {
  it('opens the home page', () => {
    cy.visit('/')
    cy.contains('Home Page').should('be.visible')
  })
})
