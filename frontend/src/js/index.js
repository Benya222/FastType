import { ApiService } from "./service";
import { TypingBox } from "./typing-box";
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
const textListEl = document.getElementById("searchResultList");

// ==== Init Custom Instruments ========================= //
const service = new ApiService();
const typingBox = new TypingBox();

// ==== Start Page With Words ======================= //
fetchWordsByOptions().then((words) => (typingBox.content = words.data));
repeatBtnEl.addEventListener("click", () => {
  fetchWordsByOptions().then((words) => (typingBox.content = words.data));
});

// ==== Choose Words Or Text ======================== //
chooseOptionEl.forEach((radio) => {
  radio.addEventListener("change", selectOption);
});

// ==== Choose Words ========================= //
wordsOptionsEl.addEventListener("change", (evt) => {
  if (evt.target.nodeName !== "INPUT") {
    return;
  }

  typingBox.focus();
  fetchWordsByOptions().then((words) => (typingBox.content = words.data));
});

// ==== Handle Text Modal ========================= //
openTextModalEl.addEventListener("click", onOpenTextModal);
closeTextModalEl.addEventListener("click", onCloseTextModal);

// ==== Handle Search Text ========================== //
textSearchBtnEl.addEventListener("click", () => {
  fetchTextsByParams().then((texts) => changeTextItems(texts.data));
});

// ==== Handle Filter Modal ====================== //
openFilterModalEl.addEventListener("click", () => {
  filterModalEl.hidden = !filterModalEl.hidden;
});

filterModalBtnEl.addEventListener("click", () => {
  filterModalEl.hidden = true;
  fetchTextsByParams().then((texts) => changeTextItems(texts.data));
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
fetchTextsByParams().then((texts) => changeTextItems(texts.data));

// ==== Callback And Helper Functions ============= //
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
  } else {
    wordsOptionsEl.hidden = true;
    textOptionsEl.hidden = false;
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
