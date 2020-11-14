export { };

type T = Window & typeof globalThis;

declare global {
    interface Window extends T {
        ymaps: any;
    }
}
