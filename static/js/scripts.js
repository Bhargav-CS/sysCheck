document.getElementById('capture-btn').addEventListener('click', function() {
    fetch('/screenshot')
        .then(response => response.json())
        .then(data => {
            const downloadBtn = document.getElementById('download-btn');
            const screenshotImg = document.getElementById('screenshot-img');
            const generateBtn = document.getElementById('generate-btn');
            
            downloadBtn.style.display = 'block';
            downloadBtn.href = data.url;
            downloadBtn.download = 'screenshot.png';
            
            screenshotImg.style.display = 'block';
            screenshotImg.src = data.url;

            generateBtn.style.display = 'block';
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('generate-btn').addEventListener('click', function() {
    const loadingDiv = document.getElementById('loading');
    const descriptionDiv = document.getElementById('description');
    
    loadingDiv.style.display = 'block';
    descriptionDiv.style.display = 'none';
    descriptionDiv.innerHTML = '';

    fetch('/generate')
        .then(response => response.json())
        .then(data => {
            loadingDiv.style.display = 'none';
            descriptionDiv.style.display = 'block';
            descriptionDiv.innerHTML = data.description;
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            descriptionDiv.style.display = 'block';
            descriptionDiv.innerHTML = 'Error generating description';
            console.error('Error:', error);
        });
});