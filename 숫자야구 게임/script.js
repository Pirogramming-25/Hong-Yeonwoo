let answer = [];
let attempts = 9;

const number1 = document.getElementById("number1");
const number2 = document.getElementById("number2");
const number3 = document.getElementById("number3");
const attemptsSpan = document.getElementById("attempts");
const results = document.getElementById("results");
const resultImg = document.getElementById("game-result-img");
const submitButton = document.querySelector(".submit-button");

function startGame() {
    attempts = 9;
    answer = makeAnswer();   // 제출 전에는 반드시 랜덤 생성!

    attemptsSpan.textContent = attempts;
    results.innerHTML = "";
    resultImg.style.display = "none";
    resultImg.src = "";

    clearInputs();
    number1.focus();

    console.log("정답:", answer);
}

function makeAnswer() {
    const numbers = [];

    while (numbers.length < 3) {
        const randomNumber = Math.floor(Math.random() * 10);

        if (!numbers.includes(randomNumber)) {
            numbers.push(randomNumber);
        }
    }

    return numbers;
}

function check_numbers() {
    const inputs = [number1.value, number2.value, number3.value];

    if (inputs.includes("")) {
        clearInputs();
        number1.focus();
        return;
    }

    const userNumbers = inputs.map(Number);

    let strike = 0;
    let ball = 0;

    for (let i = 0; i < 3; i++) {
        if (userNumbers[i] === answer[i]) {
            strike++;
        } else if (answer.includes(userNumbers[i])) {
            ball++;
        }
    }

    attempts--;
    attemptsSpan.textContent = attempts;

    addResult(userNumbers, strike, ball);

    if (strike === 3) {
        clearInputs();
        endGame("success.png");
        return;
    }

    if (attempts === 0) {
        clearInputs();
        endGame("fail.png");
        return;
    }

    clearInputs();
    number1.focus();
}



function addResult(userNumbers, strike, ball) {
    const resultLine = document.createElement("div");
    resultLine.className = "check-result";

    let resultHTML = "";

    if (strike === 0 && ball === 0) {
        resultHTML = `
            <span style="display:inline-block; width:90px; text-align:center;">
                <span style="visibility:hidden;">0</span>
                <span class="num-result strike" style="visibility:hidden;">S</span>
                <span style="visibility:hidden;">0</span>
                <span class="num-result out">O</span>
            </span>
        `;
    } else {
        resultHTML = `
            <span style="display:inline-block; width:90px; text-align:center;">
                ${strike}
                <span class="num-result strike">S</span>
                ${ball}
                <span class="num-result ball">B</span>
            </span>
        `;
    }

    resultLine.innerHTML = `
        <div class="left" style="margin-right:100px;">
            ${userNumbers.join(" ")}
        </div>

        <div>:</div>

        <div class="right" style="margin-left:100px;">
            ${resultHTML}
        </div>
    `;

    results.appendChild(resultLine);
}

function endGame(imageName) {
    resultImg.src = imageName;
    resultImg.style.display = "block";
    submitButton.disabled = true;
}

function clearInputs() {
    number1.value = "";
    number2.value = "";
    number3.value = "";
}

startGame();