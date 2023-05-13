const sinon = require('sinon');
const fs = require('fs');
const path = require('path');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync(path.resolve(__dirname, '..', 'add_candidate.html'), 'utf8');
let dom;
let container;

describe('validateForm', () => {
  beforeEach(() => {
    dom = new JSDOM(html, { runScripts: 'dangerously' });
    container = dom.window.document;
  });

  const fillForm = (candidateName, id, ballot) => {
    container.querySelector('input[name="candidate_name"]').value = candidateName;
    container.querySelector('input[name="id"]').value = id;
    container.querySelector('input[name="ballot"]').value = ballot;
  };

  it('shows an error if no candidate name is provided', () => {
    fillForm('', '123', '456');
    const submitButton = container.querySelector('button[type="submit"]');
    const form = container.querySelector('form');
    const submitStub = sinon.stub(form, 'submit');

    submitButton.click();

    expect(submitStub.called).to.be.false;
  });

  it('shows an error if no ID is provided', () => {
    fillForm('John Doe', '', '456');
    const submitButton = container.querySelector('button[type="submit"]');
    const form = container.querySelector('form');
    const submitStub = sinon.stub(form, 'submit');

    submitButton.click();

    expect(submitStub.called).to.be.false;
  });

  it('shows an error if no Vote ballot ID is provided', () => {
    fillForm('John Doe', '123', '');
    const submitButton = container.querySelector('button[type="submit"]');
    const form = container.querySelector('form');
    const submitStub = sinon.stub(form, 'submit');

    submitButton.click();

    expect(submitStub.called).to.be.false;
  });

  it('submits the form if all fields are filled', () => {
    fillForm('John Doe', '123', '456');
    const submitButton = container.querySelector('button[type="submit"]');
    const form = container.querySelector('form');
    const submitStub = sinon.stub(form, 'submit');

    submitButton.click();

    expect(submitStub.called).to.be.true;
  });
});
