import isJsonString from './isJsonString';

class LocalStorageObject {
  #storageId;
  #object;

  constructor(storageId) {
    this.#storageId = storageId;
    const data = window.localStorage.getItem(`${this.#storageId}`);
    this.#object = (isJsonString(data) && JSON.parse(data)) || {};
  }

  getValue(key) {
    return this.#object[key];
  }

  setValue(key, val) {
    this.#object[key] = val;
    window.localStorage.setItem(
      `${this.#storageId}`,
      JSON.stringify(this.#object),
    );
  }
}

export default LocalStorageObject;
