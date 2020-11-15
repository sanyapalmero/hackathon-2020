interface Asset {
    asset_info: string,
    coordinates: string | null,
}

export default class YandexMap {
    baseElement: HTMLElement;

    constructor(baseElement: HTMLElement) {
        this.baseElement = baseElement;

        let coordinates = this.baseElement.getAttribute('data-coordinates');
        let assets = this.baseElement.getAttribute("data-assets");

        // Инициализация карты для одного объекта
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
                        iconColor: '#e95420'
                    })
                )
            });
        }

        // Инициализация карты для группы объектов
        if (assets) {
            window.ymaps.ready().then(() => {
                let map = new window.ymaps.Map(this.baseElement, {
                    center: [51.768011, 55.096929], // Координаты центра Оренбурга
                    zoom: 7,
                });
                let assetsList = JSON.parse(assets!) as Asset[];
                for (let asset of assetsList) {
                    if (asset.coordinates) {
                        let splittedCoordinates = asset.coordinates.split(" ");
                        let latitude = Number(splittedCoordinates[0]);
                        let longitude = Number(splittedCoordinates[1]);
                        map.geoObjects.add(
                            new window.ymaps.Placemark(
                                [latitude, longitude],
                                {
                                    balloonContent: asset.asset_info,
                                },
                                {
                                    preset: 'islands#greenDotIconWithCaption',
                                    iconColor: '#e95420'
                                }
                            )
                        )
                    }
                }
            });
        }
    }
}
