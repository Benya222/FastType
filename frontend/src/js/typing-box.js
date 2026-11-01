import { countCpm, countAccuracy, countScore, formatTime } from "./utils";

export class TypingBox {
  #content;
  constructor() {
    this.contentDisplay = document.getElementById("textDisplay");
    this.userInput = document.getElementById("userInput");

    this.#content = "";
    this.chars = [];

    this.startTime = null;
    this.spentTime = null;

    this.userInput.addEventListener("input", this.handleUserInput);
    this.userInput.addEventListener("keydown", (evt) => {
      if (evt.key === "Backspace" || evt.key === "Delete") {
        evt.preventDefault();
      }
    });
  }

  get content() {
    return this.#content;
  }

  set content(content) {
    this.#content = content;

    this.reset();

    const fragment = document.createDocumentFragment();

    for (let i = 0; i < content.length; i++) {
      const span = document.createElement("span");
      span.textContent = content[i];
      fragment.append(span);
      this.chars.push(span);
    }

    this.contentDisplay.append(fragment);
    this.chars[0]?.classList.add("char-current");
  }

  handleUserInput = () => {
    const typed = this.userInput.value;
    const currentPosition = typed.length - 1;
    const currentTyped = typed[currentPosition];
    const currentSpan = this.chars[currentPosition];

    if (typed.length === 1) {
      this.startTime = Date.now();
    }

    if (typed.length > 0) {
      this.enableFocusMode();
    }

    currentSpan.className = "";

    if (currentTyped === currentSpan.textContent) {
      currentSpan.classList.add("char-correct");
    } else {
      currentSpan.classList.add("char-incorrect");
    }

    this.chars[currentPosition + 1]?.classList.add("char-current");

    this.updateScroll();

    if (typed.length >= this.chars.length) {
      this.inputFinish();
    }
  };

  updateScroll() {
    const typedLength = this.userInput.value.length;

    if (!this.chars.length) return;

    // Символ, который пользователь сейчас набирает,
    // либо последний символ, если текст уже закончен.
    const index = Math.min(typedLength, this.chars.length - 1);

    const currentSpan = this.chars[index];
    const firstSpan = this.chars[0];

    if (!currentSpan || !firstSpan) return;

    const lineHeight = parseFloat(
      getComputedStyle(this.contentDisplay).lineHeight,
    );

    // Определяем номер строки, начиная с нуля.
    // Transform сдвигает оба элемента одинаково,
    // поэтому разница координат остаётся корректной.
    const currentTop = currentSpan.getBoundingClientRect().top;
    const firstTop = firstSpan.getBoundingClientRect().top;

    const lineIndex = Math.max(
      0,
      Math.round((currentTop - firstTop) / lineHeight),
    );

    // Первые две строки не прокручиваем.
    // Начиная с третьей, сдвигаем текст так,
    // чтобы текущая строка оставалась посередине.
    const offset = Math.max(0, lineIndex - 1) * lineHeight;

    this.contentDisplay.style.transform = `translateY(-${offset}px)`;
  }

  focus() {
    this.userInput.focus();
  }

  reset() {
    this.contentDisplay.replaceChildren();
    this.contentDisplay.style.transform = "translateY(0)";

    this.userInput.value = "";
    this.userInput.readOnly = false;

    this.startTime = null;
    this.spentTime = null;

    this.chars = [];
  }

  inputFinish() {
    const endTime = Date.now();
    this.spentTime = (endTime - this.startTime) / 1000;
    this.updateResults();
    this.userInput.readOnly = true;
    this.disableFocusMode();

    this.content = this.#content;
  }

  enableFocusMode() {
    document.body.classList.add("focus-mode");
    document.addEventListener("click", this.handleDocumentClick);
  }

  disableFocusMode() {
    document.body.classList.remove("focus-mode");
    document.removeEventListener("click", this.handleDocumentClick);
  }

  handleDocumentClick = (evt) => {
    if (!evt.target.closest(".typing__box")) {
      this.disableFocusMode();
    }
  };

  updateResults() {
    const timeEl = document.getElementById("resultTime");
    const symbolsEl = document.getElementById("resultSymbols");
    const speedEl = document.getElementById("resultSpeed");
    const accuracyEl = document.getElementById("resultAccuracy");
    const scoreEl = document.getElementById("resultScore");

    const time = formatTime(this.spentTime);
    const symbols = this.#content.length;
    const speed = countCpm(this.spentTime, this.#content.length);
    const accuracy = countAccuracy(this.#content, this.userInput.value);
    const score = countScore(speed, accuracy);

    timeEl.textContent = time;
    symbolsEl.textContent = String(symbols);
    speedEl.textContent = String(speed);
    accuracyEl.textContent = String(accuracy);
    scoreEl.textContent = String(score);
  }
}
