/* Hide containers of pre elements containing only empty spans */
document.addEventListener("DOMContentLoaded", function() {
  const preElements = document.querySelectorAll('pre');
  preElements.forEach(function(preElement) {
    const parentElement = preElement.parentElement;
    const grandparentElement = parentElement.parentElement;
    if (parentElement && parentElement.tagName === 'DIV' &&
        grandparentElement && grandparentElement.tagName === 'DIV' &&
        grandparentElement.textContent.trim() === '') {
      grandparentElement.classList.add('hidden');
    }
  });
});
