// 最初の科目(カード)を開く
document.querySelector("button[class*=TodoCard]").click();
// exam ぽそうか判定
if(document.querySelector("p[class*=TodoAnnouncement__Description]>strong[class*=TodoAnnouncement__Title]").textContent === "確認テスト"){
    console.log("");
}


// exam ぽい
// --> 親要素のボタンを削除する