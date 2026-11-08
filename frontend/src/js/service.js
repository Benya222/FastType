const BASE_URL = "http://127.0.0.1:5000/api";

export class ApiService {
  constructor() {
    this.wordsContent = null;
    this.textContent = null;

    this.textQuery = null;
    this.minWords = null;
    this.maxWords = null;
    this.page = 1;
  }

  async fetchWords(difficult, count) {
    const res = await fetch(
      `${BASE_URL}/words?difficult=${difficult}&count=${count}`,
    );
    const words = await res.json();
    this.wordsContent = words.data;
    return words;
  }

  async fetchTexts(params) {
    if (
      params.q !== this.textQuery ||
      params.from_w_count !== this.minWords ||
      params.to_w_count !== this.maxWords
    ) {
      this.page = 1;
    }

    this.textQuery = params.q;
    this.minWords = params.from_w_count;
    this.maxWords = params.to_w_count;

    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== "") {
        searchParams.append(key, value);
      }
    });
    const res = await fetch(
      `${BASE_URL}/text?${searchParams.toString()}&page=${this.page}`,
    );
    this.page++;
    return await res.json();
  }

  async fetchTextById(id) {
    const res = await fetch(`${BASE_URL}/text/${id}`);
    const data = await res.json();
    this.textContent = data.data.text;
    return data;
  }
}
