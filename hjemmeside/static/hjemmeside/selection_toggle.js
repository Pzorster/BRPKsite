function toggleSection(sectionId, displayType = 'block') {
            const content = document.getElementById('content-' + sectionId);
            const arrow = document.getElementById('arrow-' + sectionId);
            
            if (content.style.display === 'none') {
                content.style.display = displayType;
                arrow.textContent = '▲';
            } else {
                content.style.display = 'none';
                arrow.textContent = '▼';
            }
        }