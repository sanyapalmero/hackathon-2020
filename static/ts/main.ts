import "../scss/main.scss";

import $ from 'jquery';
import 'bootstrap';
import bsCustomFileInput from 'bs-custom-file-input'
import Swiper, {Navigation, Pagination} from "swiper";


// Local
import ModalValue from './components/ModalValue';
import YandexMap from './components/YandexMap';
import DemoFill from "./components/DemoFill";
import ResetInputElement from "./components/ResetInputElement";


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

$('.DemoFill').each((index, htmlElement) => {
    new DemoFill(htmlElement);
});

$(".ResetInput").each((index, htmlElement) => {
    new ResetInputElement(htmlElement);
});

Swiper.use([Navigation, Pagination]);

new Swiper('.swiper-container', {
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});
