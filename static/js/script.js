/**
 * Update syntax highlighting for a textarea
 */
function updateHighlight(textareaId, highlightId) {
    const textarea = document.getElementById(textareaId);
    const highlight = document.getElementById(highlightId);
    const code = textarea.value;
    
    highlight.textContent = code;
    hljs.highlightElement(highlight);
}

/**
 * Refactor code by sending it to the Flask backend
 * 
 * TODO: This is where the refactoring happens
 * The function sends the original code to the /refactor endpoint
 * and displays the refactored code in the output textarea
 */
async function refactorCode() {
    const originalCode = document.getElementById('originalCode').value.trim();
    const refactorBtn = document.getElementById('refactorBtn');
    const btnText = refactorBtn.querySelector('.btn-text');
    const spinner = refactorBtn.querySelector('.spinner');
    const statusMessage = document.getElementById('statusMessage');
    
    // Validate input
    if (!originalCode) {
        showStatus('Please enter some code to refactor!', 'error');
        return;
    }
    
    // Disable button and show loading state
    refactorBtn.disabled = true;
    btnText.style.display = 'none';
    spinner.style.display = 'inline-block';
    statusMessage.style.display = 'none';
    
    try {
        // Send POST request to /refactor endpoint
        const response = await fetch('/refactor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: originalCode })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Success - display refactored code
            document.getElementById('refactoredCode').value = data.refactored_code;
            updateHighlight('refactoredCode', 'refactoredCodeHighlight');
            showStatus('Code refactored successfully!', 'success');
        } else {
            // Error from server
            showStatus(`Error: ${data.error || 'Unknown error occurred'}`, 'error');
        }
        
    } catch (error) {
        // Network or other error
        showStatus(`Error: ${error.message}`, 'error');
        console.error('Error:', error);
    } finally {
        // Re-enable button
        refactorBtn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
    }
}

/**
 * Clear the input textarea
 */
function clearInput() {
    document.getElementById('originalCode').value = '';
    document.getElementById('originalCodeHighlight').textContent = '';
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
    } catch (error) {
        // Fallback for older browsers
        const textarea = document.getElementById('refactoredCode');
        textarea.select();
        document.execCommand('copy');
        showStatus('Code copied to clipboard!', 'success');
    }
}

/**
 * Show status message to user
 * @param {string} message - Message to display
 * @param {string} type - Type of message: 'success', 'error', or 'info'
 */
function showStatus(message, type) {
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.style.display = 'block';
    
    // Auto-hide success messages after 3 seconds
    if (type === 'success') {
        setTimeout(() => {
            statusMessage.style.display = 'none';
        }, 3000);
    }
}

// Allow Ctrl+Enter to trigger refactoring
document.getElementById('originalCode').addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 'Enter') {
        event.preventDefault();
        refactorCode();
    }
});

// Sync scroll between textarea and highlight
document.getElementById('originalCode').addEventListener('scroll', function() {
    const highlight = document.getElementById('originalCodeHighlight');
    highlight.style.transform = `translate(-${this.scrollLeft}px, -${this.scrollTop}px)`;
});

document.getElementById('refactoredCode').addEventListener('scroll', function() {
    const highlight = document.getElementById('refactoredCodeHighlight');
    highlight.style.transform = `translate(-${this.scrollLeft}px, -${this.scrollTop}px)`;
});
