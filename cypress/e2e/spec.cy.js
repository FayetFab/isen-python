describe('Create and connect to an account', () => {
  it('Visits the Oc commerce site', () => {
    cy.visit('/home')

    // User is able to create an account an to be redirect to login pages

    cy.contains('SIGNUP').click()
    cy.url().should('include', '/user/signup')
    // cy.contains('fname')
    cy.get('[id^=fname]').type('fakeuser')
    cy.get('[id^=lname]').type('toto')
    cy.get('[id^=username]').type('fakeuser')
    cy.get('[id^=email]').type('fake@email.com')
    cy.get('[id^=pass]').type('1hstesh<23456789')
    cy.get('[id^=re_pass]').type('1hstesh<23456789')
    cy.get('form').contains('Register').click()
    cy.url().should('include', 'user/login')

    // User is able to connect with the previously created account
    cy.get('[id^=your_name]').type('fakeuser')
    cy.get('[id^=your_pass]').type('1hstesh<23456789')
    cy.get('form').contains('Log in').click()
    cy.url().should('include', '/home')
    cy.contains('FAVOURITE') 
  })
})

describe('Put item in favourite', () => {
  it('Connect to OC commerce and put in favourite', () => {

    // Step 1: Visit the home page and log in with the previously created account
    cy.visit("/home");
    cy.contains("LOGIN").click();
    cy.get("[id^=your_name]").type("fakeuser");
    cy.get("[id^=your_pass]").type("1hstesh<23456789");
    cy.get("form").contains("Log in").click();
    cy.url().should("include", "/home");

    // Step 2: Go to the 'favourite' page and verify it is empty
    cy.contains("FAVOURITE").click();
    cy.url().should("include", "/favourite");
    cy.contains("No Product in your favourite list. Please add").should(
      "be.visible"
    );

    // Step 3: Go back to the home page
    cy.contains("OC-commerce").click();
    cy.url().should("include", "/home");

    // Step 4: Hover over the heart icon and click it to add to favourites
    cy.get(".portfolio-item").first().trigger("mouseover");
    cy.get(".portfolio-item")
      .first()
      .within(() => {
        cy.get("a").click();
      });

    // Step 5: Go back to the 'favourite' page and verify the item is added
    cy.contains("FAVOURITE").click();
    cy.url().should("include", "/favourite");

    // Step 6: Delete the item from favourites
    cy.get("td").contains("milk bread").should("exist");
    cy.get("td").contains("milk bread").parents("tr").find("a").click();

    // Step 7: Go back to the 'favourite' page and confirm the item has been deleted
    cy.contains("FAVOURITE").click();
    cy.url().should("include", "/favourite");
    cy.contains("No Product in your favourite list. Please add").should(
      "be.visible"
    );

  })
})