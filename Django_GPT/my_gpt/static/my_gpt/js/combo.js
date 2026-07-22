const form = document.getElementById("combo-form");
const textInput = document.getElementById("text");
const submitButton = form.querySelector("button[type='submit']");
const regenerateButton = document.getElementById("regenerate-button");
const resultBox = document.getElementById("result");

let lastInputText = "";

function setLoading(isLoading) {
    submitButton.disabled = isLoading;
    regenerateButton.disabled = isLoading || !lastInputText;
    textInput.disabled = isLoading;
    submitButton.textContent = isLoading ? "처리 중..." : "복합 분석하기";
}

async function runComboAnalysis(inputText, loadingMessage = "처리 중...") {
    resultBox.style.display = "block";

    if (inputText.length < 200) {
        resultBox.innerHTML = `<p class="error">복합 분석할 문서는 200자 이상 입력해주세요.</p>`;
        return;
    }

    if (inputText.length > 5000) {
        resultBox.innerHTML = `<p class="error">문서는 5,000자 이하로 입력해주세요.</p>`;
        return;
    }

    const formData = new FormData(form);
    formData.set("text", inputText);

    setLoading(true);
    resultBox.textContent = loadingMessage;

    try {
        const response = await fetch("/api/combo/", {
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

        const toxicityScores = data.toxicity.scores
            .map((item) => `${item.label}: ${item.score}%`)
            .join("\n");

        resultBox.innerHTML = `
            <h2>분석 결과</h2>
            <div class="score-list"><strong>입력 원문</strong>\n${data.input_text}</div>
            <div class="score-list"><strong>요약</strong>\n${data.summary}</div>
            <p><strong>감정 분석:</strong> ${data.sentiment.label} (${data.sentiment.confidence}%)</p>
            <p><strong>유해 표현 최고 레이블:</strong> ${data.toxicity.label}</p>
            <p><strong>유해 표현 점수:</strong> ${data.toxicity.score}%</p>
            <div class="score-list"><strong>유해 표현 전체 점수</strong>\n${toxicityScores}</div>
            <div class="score-list"><strong>종합 판정</strong>\n${data.judgement}</div>
        `;

        lastInputText = inputText;
        regenerateButton.disabled = false;
    } catch (error) {
        resultBox.innerHTML = `<p class="error">모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.</p>`;
    } finally {
        setLoading(false);
    }
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();
    await runComboAnalysis(textInput.value.trim(), "처리 중...");
});

regenerateButton.addEventListener("click", async function () {
    if (!lastInputText) {
        return;
    }

    await runComboAnalysis(lastInputText, "재생성 중...");
});
