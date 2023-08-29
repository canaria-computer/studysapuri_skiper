function getFirstTodoCard() {
  return document.querySelector("button[class*=TodoCard]");
}

function findAncestorWithSelector(element, selector) {
  let currentElement = element;

  while (currentElement !== null) {
    if (currentElement.matches(selector)) {
      return currentElement;
    }
    currentElement = currentElement.parentElement;
  }

  return null;
}

function main() {
  const todoTitleElement = document.querySelector(
    "p[class*=TodoAnnouncement__Description]>strong[class*=TodoAnnouncement__Title]",
  );
  const firstTodoCard = getFirstTodoCard();

  if (todoTitleElement.textContent === "確認テスト") {
    const todoCardContainer = findAncestorWithSelector(
      todoTitleElement,
      "button[class*=TodoCard]+div",
    );

    if (todoCardContainer) {
      todoCardContainer.remove();
    }
    firstTodoCard.remove();
  }

  firstTodoCard.click();
}

main();
// TODO いい感じに繰り返す
