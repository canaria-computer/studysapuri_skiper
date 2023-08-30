const todoAnouTitleSel = "p[class*=TodoAnnouncement__Description]>strong[class*=TodoAnnouncement__Title]";

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

function examTrim() {
  const todoTitleElement = document.querySelector(todoAnouTitleSel);
  const firstTodoCard = getFirstTodoCard();

  if (todoTitleElement.textContent === "確認テスト") {
    const todoCardContainer = findAncestorWithSelector(todoTitleElement, "button[class*=TodoCard]+div");

    if (todoCardContainer) {
      todoCardContainer.remove();
    }
    firstTodoCard.remove();
  }

  firstTodoCard.click();
}

function main() {
  for (let i = 0; i < document.querySelectorAll(todoAnouTitleSel).length; i++) {
    examTrim();
  }
  if (document.querySelectorAll("div[class*=isSelected]").length <= 0) {
    getFirstTodoCard().click();
  }
}

main();
