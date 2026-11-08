import { ApiService } from "./service";
import { TypingBox } from "./typing-box";
import { formatText } from "./utils";
import noUiSlider from "nouislider";
import "nouislider/dist/nouislider.css";

const wordsOptionsEl = document.getElementById("words-options");
const textOptionsEl = document.getElementById("text-options");

const chooseOptionEl = document.querySelectorAll("input[name='words-or-text']");

const repeatBtnEl = document.getElementById("repeatBtn");

const backdropEl = document.querySelector("[data-modal]");
const openTextModalEl = document.querySelector("[data-open-modal]");
const closeTextModalEl = document.querySelector("[data-close-modal]");

// ==== Text Search Elements ========================== //
const textSearchEl = document.getElementById("textSearchInput");
const textSearchBtnEl = document.getElementById("textSearchBtn");

// ==== Text Filter Elements ======================== //
const filterModalEl = document.querySelector(".js-filter-modal");
const openFilterModalEl = document.getElementById("openFilterModal");
const filterModalBtnEl = document.getElementById("filterBtn");

const filterSliderEl = document.getElementById("filterSlider");
const filterFromCountEl = document.getElementById("filterFromCount");
const filterToCountEl = document.getElementById("filterToCount");

// ==== Text List Elements ============================ //
const scrollContainerEl = document.getElementById("scrollContainer");
const textListEl = document.getElementById("searchResultList");

// ==== Init Custom Instruments ========================= //
const service = new ApiService();
const typingBox = new TypingBox();

// ==== Text Items Observer ============================ //
const loader = document.getElementById("loader");
const observer = new IntersectionObserver(
  (entries) => {
    const entry = entries[0];
    if (entry.isIntersecting) {
      loadTextItems();
    }
  },
  {
    root: scrollContainerEl,
    rootMargin: "300px",
    threshold: 0,
  },
);
let isLoading = false;
let hasMore = true;
observer.observe(loader);

// ==== Start Page With Words ======================= //
setWords();

// ==== Choose Words Or Text ======================== //
chooseOptionEl.forEach((radio) => {
  radio.addEventListener("change", selectOption);
});

// ==== Choose Words ========================= //
wordsOptionsEl.addEventListener("change", (evt) => {
  if (evt.target.nodeName !== "INPUT") {
    return;
  }

  setWords();
  typingBox.focus();
});

repeatBtnEl.addEventListener("click", setWords);

// ==== Handle Text Modal ========================= //
openTextModalEl.addEventListener("click", onOpenTextModal);
closeTextModalEl.addEventListener("click", onCloseTextModal);

// ==== Handle Search Text ========================== //
textSearchBtnEl.addEventListener("click", () => {
  hasMore = true;
  service.page = 1;
  scrollToTop();
  loadTextItems();
});

// ==== Handle Filter Modal ====================== //
openFilterModalEl.addEventListener("click", () => {
  filterModalEl.hidden = !filterModalEl.hidden;
});

filterModalBtnEl.addEventListener("click", () => {
  filterModalEl.hidden = true;
  hasMore = true;
  service.page = 1;
  scrollToTop();
  loadTextItems();
});

noUiSlider.create(filterSliderEl, {
  start: [20, 250],
  range: {
    min: [20],
    max: [250],
  },
  connect: true,
});

filterSliderEl.noUiSlider.on("update", onSliderUpdate);

// ==== Fetch Texts =============================== //
loadTextItems();

// ==== Handle Choice Of Text ===================== //
textListEl.addEventListener("click", onTextListClick);

// ==== Callback And Helper Functions ============= //
async function setWords() {
  const data = await fetchWordsByOptions();
  typingBox.content = data.data;
}

async function setText(id) {
  const data = await service.fetchTextById(id);
  typingBox.content = formatText(data.data.text);
}

function onTextListClick(evt) {
  if (evt.target.nodeName !== "LI") {
    return;
  }

  onCloseTextModal();
  typingBox.focus();

  const textId = evt.target.dataset.id;
  setText(textId);
}

function scrollToTop() {
  scrollContainerEl.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}

async function loadTextItems() {
  if (isLoading || !hasMore) return;

  isLoading = true;
  try {
    const data = await fetchTextsByParams(30);

    if (data.data.length === 0) {
      if (Number(data.meta.page) === 1) {
        textListEl.innerHTML = `<li style="text-align: center;">Not found</li>`;
      }

      hasMore = false;
      return;
    }

    putTextItems(data);

    hasMore = data.meta.has_next;
  } catch (error) {
    console.log(error);
  } finally {
    isLoading = false;
  }
}

async function fetchTextsByParams(per_page = null) {
  const fromWordCount = Math.round(filterSliderEl.noUiSlider.get()[0]);
  const toWordCount = Math.round(filterSliderEl.noUiSlider.get()[1]);
  const query = textSearchEl.value;

  return await service.fetchTexts({
    q: query,
    from_w_count: fromWordCount,
    to_w_count: toWordCount,
    per_page: per_page,
  });
}

function putTextItems(data) {
  if (Number(data.meta.page) > 1) {
    addTextItems(data.data);
  } else {
    changeTextItems(data.data);
  }
}

function changeTextItems(texts) {
  const html = texts.map(renderItemText).join("");
  textListEl.innerHTML = html;
}

function addTextItems(texts) {
  const html = texts.map(renderItemText).join("");
  textListEl.insertAdjacentHTML("beforeend", html);
}

function renderItemText(text) {
  return `<li class="search-result__item" data-id="${text.id}">
            <span>
              ${text.title}
            </span>
            <span id="wordsCount" class="search-result__words-count">
              ${text.word_count} words
            </span>
          </li>`;
}

function onSliderUpdate(values) {
  filterFromCountEl.textContent = Math.round(values[0]);
  filterToCountEl.textContent = Math.round(values[1]);
}

async function fetchWordsByOptions() {
  const difficult = wordsOptionsEl.querySelector(
    'input[name="difficulty"]:checked',
  );
  const count = wordsOptionsEl.querySelector(
    'input[name="words-count"]:checked',
  );

  return await service.fetchWords(difficult.value, count.value);
}

function selectOption(evt) {
  if (evt.currentTarget.value === "words") {
    wordsOptionsEl.hidden = false;
    textOptionsEl.hidden = true;

    repeatBtnEl.hidden = false;

    typingBox.content = service.wordsContent;
  } else {
    wordsOptionsEl.hidden = true;
    textOptionsEl.hidden = false;

    repeatBtnEl.hidden = true;

    if (service.textContent === null) {
      setText(1);
      typingBox.focus();
      return;
    }

    typingBox.content = formatText(service.textContent);
  }

  typingBox.focus();
}

function onOpenTextModal() {
  backdropEl.classList.toggle("is-hidden");
  backdropEl.addEventListener("click", onBackdropClick);
}

function onCloseTextModal() {
  backdropEl.classList.toggle("is-hidden");
  backdropEl.removeEventListener("click", onBackdropClick);
}

function onBackdropClick(evt) {
  if (!evt.target.closest(".js-text-modal")) {
    backdropEl.classList.toggle("is-hidden");
    backdropEl.removeEventListener("click", onBackdropClick);
  }
}
