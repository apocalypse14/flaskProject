document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('pdfs');
    const fileChosen = document.getElementById('file-chosen');

    fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
            fileChosen.textContent = Array.from(fileInput.files).map(file => file.name).join(', ');
        } else {
            fileChosen.textContent = 'No file chosen';
        }
    });
});
