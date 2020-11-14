import "../scss/main.scss";

import $ from 'jquery';
import 'bootstrap';
import bsCustomFileInput from 'bs-custom-file-input'

// Local
import ModalValue from './components/ModalValue';
import YandexMap from './components/YandexMap';


// Set value for modal window
$('.ModalValue').each((_index, htmlElement) => {
  new ModalValue($(htmlElement));
});

$(function () {
  bsCustomFileInput.init()
})

$('.YandexMap').each((index, htmlElement) => {
  new YandexMap(htmlElement);
});
