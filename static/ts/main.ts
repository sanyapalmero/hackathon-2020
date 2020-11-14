import "../scss/main.scss";

import $ from 'jquery';
import 'bootstrap';


// Local
import ModalValue from './components/ModalValue';


// Set value for modal window
$('.ModalValue').each((_index, htmlElement) => {
    new ModalValue($(htmlElement));
});
