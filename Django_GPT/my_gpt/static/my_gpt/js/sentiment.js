const form = document.getElementById("sentiment-form");
const textInput = document.getElementById("text");
const submitButton = form.querySelector("button[type='submit']");
const resultBox = document.getElementById("result");
const historyList = document.getElementById("history-list");
const historyEmpty = document.getElementById("history-empty");
const isAuthenticated = document.body.dataset.authenticated === "true";
const anonymousHistories = [];

function setLoading(isLoading) {
    submitButton.disabled = isLoading;
    textInput.disabled = isLoading;
    submitButton.textContent = isLoading ? "처리 중..." : "분석하기";
}

function renderAnonymousHistories() {
    if (!historyList || isAuthenticated) {
        return;
    }

    historyList.innerHTML = anonymousHistories
        .map((history) => {
            return `
                <li>
                    <span class="history-input">${history.input}</span>
                    <span class="history-arrow">→</span>
                    <strong>${history.label}</strong>
                    <span>(${history.confidence}%)</span>
                </li>
            `;
        })
        .join("");

    if (historyEmpty) {
        historyEmpty.style.display = anonymousHistories.length ? "none" : "block";
    }
}

function addAnonymousHistory(input, label, confidence) {
    if (isAuthenticated) {
        return;
    }

    anonymousHistories.unshift({
        input: input.length > 60 ? `${input.slice(0, 57)}...` : input,
        label,
        confidence,
    });

    anonymousHistories.splice(5);
    renderAnonymousHistories();
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(form);
    const inputText = formData.get("text").trim();
    resultBox.style.display = "block";

    if (!inputText) {
        resultBox.innerHTML = `<p class="error">분석할 문장을 입력해주세요.</p>`;
        return;
    }

    setLoading(true);
    resultBox.textContent = "처리 중...";

    try {
        const response = await fetch("/api/sentiment/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
            },
        });

        const data = await response.json();

        if (!data.ok) {
            resultBox.innerHTML = `<p class="error">${data.error}</p>`;
            return;
        }

        const scores = data.scores
            .map((item) => `${item.label}: ${item.score}%`)
            .join("\n");

        resultBox.innerHTML = `
            <h2>분석 결과</h2>
            <p><strong>감정:</strong> ${data.label}</p>
            <p><strong>신뢰도:</strong> ${data.confidence}%</p>
            <div class="score-list"><strong>전체 점수</strong>\n${scores}</div>
        `;

        addAnonymousHistory(inputText, data.label, data.confidence);
    } catch (error) {
        resultBox.innerHTML = `<p class="error">모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.</p>`;
    } finally {
        setLoading(false);
    }
});
