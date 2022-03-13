// people.spec.js created with Cypress
//
// Start writing your Cypress tests below!
// If you're unfamiliar with how Cypress works,
// check out the link below and learn how to write your first test:
// https://on.cypress.io/writing-first-test

describe('People app functionality', () => {
  it('opens the login page', () => {
    cy.visit('/user/login');
    cy.contains('Email').should('be.visible');
  })

  it('can view the profile page', () => {
    cy.visit('/user/profile');
    cy.contains('Department').should('be.visible');
  })

  it('can view the mentor portal', () => {
    cy.visit('/mentor');
    cy.contains('My Mentees').should('be.visible');
  })

  it('can select a mentor', () => {
    // This test assumes that the user you are using is not currently assigned a mentor
    cy.visit('/mentee');
    cy.contains('Please choose a Mentor').should('be.visible');
    cy.get('input[type=submit]').click();
    cy.contains('Your Mentor:').should('be.visible');
  })

})
