/* Hide containers of pre elements containing only empty spans */
document.addEventListener("DOMContentLoaded", function() {
  const preElements = document.querySelectorAll('pre');
  preElements.forEach(function(preElement) {
    const childElements = preElement.children;
    if (childElements.length === 1 && childElements[0].tagName === 'SPAN' && childElements[0].textContent.trim() === '') {
      const parentElement = preElement.parentElement;
      const grandparentElement = parentElement.parentElement;
      if (parentElement && parentElement.tagName === 'DIV' &&
          grandparentElement && grandparentElement.tagName === 'DIV') {
        grandparentElement.classList.add('hidden');
      }
    }
  });
});