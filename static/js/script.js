/**
 * Update syntax highlighting for a textarea
 */
function updateHighlight(textareaId, highlightId) {
    const textarea = document.getElementById(textareaId);
    const highlight = document.getElementById(highlightId);
    highlight.textContent = textarea.value;
    hljs.highlightElement(highlight);
}

/**
 * When language changes, update highlight language class on both editors
 */
function onLanguageChange() {
    const lang = document.getElementById('languageSelect').value;
    const hlLang = lang === 'java' ? 'language-java' : 'language-python';
    ['originalCodeHighlight', 'refactoredCodeHighlight'].forEach(id => {
        const el = document.getElementById(id);
        el.className = hlLang;
        hljs.highlightElement(el);
    });
}

/**
 * Populate a report list (<ul>) with items, or show a "none" message
 */
function populateList(ulId, items) {
    const ul = document.getElementById(ulId);
    ul.innerHTML = '';
    if (!items || items.length === 0) {
        const li = document.createElement('li');
        li.className = 'report-item report-item--none';
        li.textContent = 'None detected';
        ul.appendChild(li);
        return;
    }
    items.forEach(text => {
        const li = document.createElement('li');
        li.className = 'report-item';
        li.textContent = text;
        ul.appendChild(li);
    });
}

/**
 * Main refactor function — sends code + language to /refactor and
 * renders the full architectural report (smells, patterns, improvements)
 */
async function refactorCode() {
    const originalCode = document.getElementById('originalCode').value.trim();
    const language = document.getElementById('languageSelect').value;
    const useLlm = document.getElementById('useLlm').checked;
    const refactorBtn = document.getElementById('refactorBtn');
    const btnText = refactorBtn.querySelector('.btn-text');
    const spinner = refactorBtn.querySelector('.spinner');
    const statusMessage = document.getElementById('statusMessage');

    if (!originalCode) {
        showStatus('Please enter some code to refactor!', 'error');
        return;
    }

    // Loading state
    refactorBtn.disabled = true;
    btnText.style.display = 'none';
    spinner.style.display = 'inline-block';
    statusMessage.style.display = 'none';
    document.getElementById('reportSection').style.display = 'none';

    try {
        const response = await fetch('/refactor', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: originalCode, language: language, use_llm: useLlm })
        });

        const data = await response.json();

        if (response.ok) {
            // Show refactored code
            document.getElementById('refactoredCode').value = data.refactored_code;
            updateHighlight('refactoredCode', 'refactoredCodeHighlight');

            // Populate report panels
            populateList('smellsList', data.detected_smells);
            populateList('patternsList', data.suggested_patterns);
            populateList('improvementsList', data.improvements);
            document.getElementById('reportSection').style.display = 'grid';

            showStatus(`\u2713 ${data.summary}`, 'success');
        } else {
            showStatus(`Error: ${data.detail || data.error || 'Unknown error occurred'}`, 'error');
        }

    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        console.error('Error:', error);
    } finally {
        refactorBtn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
    }
}

/**
 * Clear the input textarea and report
 */
function clearInput() {
    document.getElementById('originalCode').value = '';
    document.getElementById('originalCodeHighlight').textContent = '';
    document.getElementById('reportSection').style.display = 'none';
    document.getElementById('statusMessage').style.display = 'none';
}

/**
 * Copy refactored code to clipboard
 */
async function copyToClipboard() {
    const refactoredCode = document.getElementById('refactoredCode').value;
    if (!refactoredCode.trim()) {
        showStatus('No refactored code to copy!', 'error');
        return;
    }
    try {
        await navigator.clipboard.writeText(refactoredCode);
        showStatus('Code copied to clipboard!', 'success');
    } catch {
        const textarea = document.getElementById('refactoredCode');
        textarea.select();
        document.execCommand('copy');
        showStatus('Code copied to clipboard!', 'success');
    }
}

/**
 * Show status message
 */
function showStatus(message, type) {
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.style.display = 'block';
    if (type === 'success') {
        setTimeout(() => { statusMessage.style.display = 'none'; }, 4000);
    }
}

// Ctrl+Enter shortcut
document.getElementById('originalCode').addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 'Enter') {
        event.preventDefault();
        refactorCode();
    }
});

// Sync scroll between textarea and highlight overlay
document.getElementById('originalCode').addEventListener('scroll', function() {
    document.getElementById('originalCodeHighlight').style.transform =
        `translate(-${this.scrollLeft}px, -${this.scrollTop}px)`;
});

document.getElementById('refactoredCode').addEventListener('scroll', function() {
    document.getElementById('refactoredCodeHighlight').style.transform =
        `translate(-${this.scrollLeft}px, -${this.scrollTop}px)`;
});

