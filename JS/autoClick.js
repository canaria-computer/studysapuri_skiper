var shuffleArray = (array) => {
    const cloneArray = [...array];
    for (let i = cloneArray.length - 1; i >= 0; i--) {
        let rand = Math.floor(Math.random() * (i + 1));
        let tmpStorage = cloneArray[i];
        cloneArray[i] = cloneArray[rand];
        cloneArray[rand] = tmpStorage;
    }
    return cloneArray;
};

setInterval(() => {
    shuffleArray(document.querySelectorAll("[class*=TopicsPage__Main]  button"))
        .forEach(each => each.click());
})

setInterval(() => {
    document.querySelector('button[class*=RaisedButton]').click();
}, Math.random() * (10000 - 1000) + 1000)