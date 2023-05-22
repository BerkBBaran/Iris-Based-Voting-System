// Import required libraries
const sinon = require('sinon');
const fs = require('fs');
const path = require('path');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const { expect } = require('chai');

// Read HTML file content
const html = fs.readFileSync(path.resolve(__dirname, '..', 'add_candidate.html'), 'utf8');
let dom;
let container;

// Describe block to group related tests
describe('validateForm', () => {
  beforeEach(() => {
    // Set up JSDOM environment
    dom = new JSDOM(html, { runScripts: 'dangerously' });
    container = dom.window.document;
  });

  // Helper function to fill the form fields
  const fillForm = (candidateName, id, ballot) => {
    container.querySelector('input[name="candidate_name"]').value = candidateName;
    container.querySelector('input[name="id"]').value = id;
    container.querySelector('input[name="ballot"]').value = ballot;
  };

  // Test case: shows an error if no candidate name is provided
  it('shows an error if no candidate name is provided', () => {
    fillForm('', '123', '456');
    const submitButton = container.querySelector('button[type="submit"]');
    const form = container.querySelector('form');
    const submitStub = sinon.stub(form, 'submit');

    submitButton.click();

    // Assertion: submit function should not be called
    expect(submitStub.called).to.be.false;
  });

  // Test case: shows an error if no ID is provided
  it('shows an error if no ID is provided', () => {
    fillForm('John Doe', '', '456');
    const submitButton = container.querySelector('button[type="submit"]');
    const form = container.querySelector('form');
    const submitStub = sinon.stub(form, 'submit');

    submitButton.click();

    // Assertion: submit function should not be called
    expect(submitStub.called).to.be.false;
  });

  // Test case: shows an error if no Vote ballot ID is provided
  it('shows an error if no Vote ballot ID is provided', () => {
    fillForm('John Doe', '123', '');
    const submitButton = container.querySelector('button[type="submit"]');
    const form = container.querySelector('form');
    const submitStub = sinon.stub(form, 'submit');

    submitButton.click();

    // Assertion: submit function should not be called
    expect(submitStub.called).to.be.false;
  });

  // Test case: submits the form if all fields are filled
  it('submits the form if all fields are filled', () => {
    fillForm('John Doe', '123', '456');
    const submitButton = container.querySelector('button[type="submit"]');
    const form = container.querySelector('form');
    const submitStub = sinon.stub(form, 'submit');

    submitButton.click();

    // Assertion: submit function should be called
    expect(submitStub.called).to.be.true;
  });
});
