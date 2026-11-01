const BASE_URL = "http://127.0.0.1:5000/api";

export class ApiService {
  counstructor() {
    this.content = null;
    this.page = 1;
  }

  async fetchWords(difficult, count) {
    const res = await fetch(
      `${BASE_URL}/words?difficult=${difficult}&count=${count}`,
    );
    const words = await res.json();
    this.content = words.data;
    return words;
  }

  async fetchTexts(params) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== "") {
        searchParams.append(key, value);
      }
    });
    const res = await fetch(`${BASE_URL}/text?${searchParams.toString()}`);
    return await res.json();
  }
}
