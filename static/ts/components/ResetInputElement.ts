export default class ResetInputElement {
    baseElement: HTMLElement;

    constructor(baseElement: HTMLElement) {
        this.baseElement = baseElement;

        let targetInputs = this.baseElement.getAttribute("data-target-input")
        if (!targetInputs) return;

        this.baseElement.addEventListener("click", ()=>{
            // TODO: Конкретизировать запрос
            document.querySelectorAll(targetInputs!).forEach((element)=>{
                element.setAttribute("value", "")
            })
        })
    }
}
