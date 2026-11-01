export function countCpm(time, content_length) {
  return Math.round((content_length / time) * 60);
}

export function countAccuracy(original, typed) {
  let correct = 0;

  const total = Math.max(original.length, typed.length);

  for (let i = 0; i < total; i++) {
    if (original[i] === typed[i]) {
      correct++;
    }
  }

  return total === 0 ? 100 : Math.round((correct / total) * 100);
}

export function countScore(cpm, accuracy) {
  return ((cpm * accuracy) / 100).toFixed(2);
}

export function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);

  return `${String(minutes).padStart(2, "0")}:${String(remainingSeconds).padStart(2, "0")}`;
}
