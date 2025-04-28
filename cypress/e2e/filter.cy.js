describe("Price Filter Form Test", () => {
  beforeEach(() => {
    cy.visit("/home");
  });

  it("should filter prices between 80 and 100", () => {
    cy.get("#min_price").clear().type("80");
    cy.get("#max_price").clear().type("100");

    cy.get('button[type="submit"]').click();

    cy.url().should("include", "min_price=80");
    cy.url().should("include", "max_price=100");

    cy.get(".portfolio-item").each(($product) => {
      cy.wrap($product)
        .find("h6")
        .invoke("text")
        .then((text) => {
          const price = parseFloat(text.replace("$", "").trim());
          expect(price).to.be.gte(80);
          expect(price).to.be.lte(100);
        });
    });
  });

  it("should sort products by price in ascending order", () => {
    cy.get('select[name="sort"]').select("asc");
    cy.get('button[type="submit"]').click();

    cy.url().should("include", "sort=asc");

    let previousPrice = 0;

    cy.get(".portfolio-item h6").each(($el) => {
      const priceText = $el.text();
      const price = parseFloat(priceText.replace("$", "").trim());

      expect(price).to.be.at.least(previousPrice);
      previousPrice = price;
    });
  });

  it("should sort products by price in descending order", () => {
    cy.get('select[name="sort"]').select("desc");
    cy.get('button[type="submit"]').click();

    cy.url().should("include", "sort=desc");

    let previousPrice = Infinity;

    cy.get(".portfolio-item h6").each(($el) => {
      const priceText = $el.text();
      const price = parseFloat(priceText.replace("$", "").trim());

      expect(price).to.be.at.most(previousPrice);
      previousPrice = price;
    });
  });

  it("should not show products outside the price range of 80-100", () => {
    cy.get("#min_price").clear().type("80");
    cy.get("#max_price").clear().type("100");
    cy.get('button[type="submit"]').click();

    cy.url().should("include", "min_price=80").and("include", "max_price=100");

    cy.get(".portfolio-item h6").each(($el) => {
      const priceText = $el.text();
      const price = parseFloat(priceText.replace("$", "").trim());

      expect(price).to.be.gte(80);
      expect(price).to.be.lte(100);
    });
  });
});