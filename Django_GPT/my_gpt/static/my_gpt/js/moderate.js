const form = document.getElementById("moderate-form");
const textInput = document.getElementById("text");
const submitButton = form.querySelector("button[type='submit']");
const resultBox = document.getElementById("result");

function setLoading(isLoading) {
    submitButton.disabled = isLoading;
    textInput.disabled = isLoading;
    submitButton.textContent = isLoading ? "처리 중..." : "분석하기";
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

    if (inputText.length > 1000) {
        resultBox.innerHTML = `<p class="error">문장은 1,000자 이하로 입력해주세요.</p>`;
        return;
    }

    setLoading(true);
    resultBox.textContent = "처리 중...";

    try {
        const response = await fetch("/api/moderate/", {
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
            <p><strong>최고 위험 레이블:</strong> ${data.label}</p>
            <p><strong>위험 점수:</strong> ${data.score}%</p>
            <div class="score-list"><strong>전체 점수</strong>\n${scores}</div>
        `;
    } catch (error) {
        resultBox.innerHTML = `<p class="error">모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.</p>`;
    } finally {
        setLoading(false);
    }
});
