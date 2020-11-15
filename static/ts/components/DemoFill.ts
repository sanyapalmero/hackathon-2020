import $ from 'jquery';

export default class DemoFill {
  baseElement: HTMLElement;

  constructor(baseElement: HTMLElement) {
    this.baseElement = baseElement;

    this.baseElement.addEventListener('click', () => {
      let email = this.baseElement.getAttribute('data-email')!;
      let password = this.baseElement.getAttribute('data-password')!;

      $('[name=email]').val(email);
      $('[name=password]').val(password);
    });
  }
}
