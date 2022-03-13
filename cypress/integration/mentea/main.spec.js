// main.spec.js created with Cypress
//
// Start writing your Cypress tests below!
// If you're unfamiliar with how Cypress works,
// check out the link below and learn how to write your first test:
// https://on.cypress.io/writing-first-test

describe('Main app functionality', () => {
  it('opens the home page', () => {
    cy.visit('/');
    cy.contains('mentoring made easy.').should('be.visible');
  })

  it('opens the faq page' , () => {
    cy.visit('/faq');
    cy.contains('Frequently Asked Questions').should('be.visible');
    cy.contains('What are Plans of Action?').click();
    cy.contains('Plans of Action are ways for mentors and mentees').should('be.visible');
  })

  it('opens the privacy policy page' , () => {
    cy.visit('/privacy');
    cy.contains('Your data protection rights').should('be.visible');
  })

  it('opens the tos page' , () => {
    cy.visit('/terms-of-service');
    cy.contains('This website contains material').should('be.visible');
  })

})
