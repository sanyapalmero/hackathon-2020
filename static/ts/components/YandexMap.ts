export default class YandexMap {
    baseElement: HTMLElement;

    constructor(baseElement: HTMLElement) {
        this.baseElement = baseElement;

        let coordinates = this.baseElement.getAttribute('data-coordinates');

        if (coordinates) {
            let splittedCoordinates = coordinates.split(" ");
            let latitude = Number(splittedCoordinates[0]);
            let longitude = Number(splittedCoordinates[1]);

            window.ymaps.ready().then(() => {
                let map = new window.ymaps.Map(this.baseElement, {
                    center: [latitude, longitude],
                    zoom: 15,
                });
                map.geoObjects.add(
                    new window.ymaps.Placemark([latitude, longitude], {}, {
                        preset: 'islands#greenDotIconWithCaption',
                        iconColor: 'red'
                    })
                )
            });
        }
    }
}
