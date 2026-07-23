const form = document.getElementById("summarize-form");
const textInput = document.getElementById("text");
const submitButton = form.querySelector("button[type='submit']");
const resultBox = document.getElementById("result");

function setLoading(isLoading) {
    submitButton.disabled = isLoading;
    textInput.disabled = isLoading;
    submitButton.textContent = isLoading ? "처리 중..." : "요약하기";
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(form);
    const inputText = formData.get("text").trim();
    resultBox.style.display = "block";

    if (inputText.length < 100) {
        resultBox.innerHTML = `<p class="error">요약할 문서는 100자 이상 입력해주세요.</p>`;
        return;
    }

    if (inputText.length > 5000) {
        resultBox.innerHTML = `<p class="error">문서는 5,000자 이하로 입력해주세요.</p>`;
        return;
    }

    setLoading(true);
    resultBox.textContent = "처리 중...";

    try {
        const response = await fetch("/api/summarize/", {
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

        resultBox.innerHTML = `
            <h2>요약 결과</h2>
            <p><strong>원문 길이:</strong> ${data.original_length}자</p>
            <p><strong>요약문 길이:</strong> ${data.summary_length}자</p>
            <p><strong>요약 비율:</strong> ${data.summary_ratio}%</p>
            <div class="score-list"><strong>요약 결과</strong>\n${data.summary}</div>
        `;
    } catch (error) {
        resultBox.innerHTML = `<p class="error">모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.</p>`;
    } finally {
        setLoading(false);
    }
});
