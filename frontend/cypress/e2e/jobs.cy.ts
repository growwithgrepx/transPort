describe('Jobs Page E2E', () => {
  it('renders jobs from the API response', () => {
    // Intercept the jobs API call and provide mock data
    cy.intercept('GET', '/jobs/table*', {
      statusCode: 200,
      body: {
        items: [
          {
            id: 1,
            customer_name: 'Alice Example',
            pickup_location: 'Central Station',
            dropoff_location: 'City Hall',
            status: 'Active',
            payment_status: 'Pending',
            date: '2024-06-01',
          },
          {
            id: 2,
            customer_name: 'Bob Test',
            pickup_location: 'Airport',
            dropoff_location: 'Harbor',
            status: 'Completed',
            payment_status: 'Paid',
            date: '2024-06-02',
          },
        ],
        total: 2,
        page: 1,
        per_page: 10,
        pages: 1,
      },
    }).as('getJobs');

    // Visit the jobs page
    cy.visit('/jobs');

    // Wait for the API call
    cy.wait('@getJobs');

    // Assert that the mock data is rendered in the table
    cy.contains('Alice Example').should('be.visible');
    cy.contains('Central Station').should('be.visible');
    cy.contains('City Hall').should('be.visible');
    cy.contains('Active').should('be.visible');
    cy.contains('Pending').should('be.visible');
    cy.contains('2024-06-01').should('be.visible');

    cy.contains('Bob Test').should('be.visible');
    cy.contains('Airport').should('be.visible');
    cy.contains('Harbor').should('be.visible');
    cy.contains('Completed').should('be.visible');
    cy.contains('Paid').should('be.visible');
    cy.contains('2024-06-02').should('be.visible');
  });
}); 